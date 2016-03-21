# -*- coding: utf-8 -*-
import urllib

import requests
from django.shortcuts import render_to_response
from django.views.decorators.gzip import gzip_page
from django.views.decorators.csrf import csrf_exempt
import math
from LYFAdmin.models import *
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.gzip import gzip_page
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q
from LYFAdmin.qq_oauth import APIClient
from LYFSite.utils import check_status
from LYFAdmin.utils import create_random_avatar
from LYFAdmin.message import REG_MES, create_new_message
from LYFAdmin.online_pay import create_alipay_order
from LeadYouFly.settings import QQ_APP_ID, QQ_APP_KEY, HOST
from models import *
import json
import utils
from PIL import Image
import os

BASE = os.path.dirname(os.path.dirname(__file__))


position_dic = {'0': u'全部位置',
                '1': u'中单',
                '2': u'上单',
                '3': u'ADC',
                '4': u'打野',
                '5': u'辅助'}

area_dic = {'0': u'全区',
            '1': u'电信',
            '2': u'网通'}


def test_kefu(req):
    return render_to_response('test.html')


def test(request):
    test_list = range(0, 11)
    paginator = Paginator(test_list, 1)
    try:
        page_num = request.GET.get('page_num')
        test_list = paginator.page(page_num)
    except PageNotAnInteger:
        test_list = paginator.page(1)
    except EmptyPage:
        test_list = paginator.page(paginator.num_pages)
    return render_to_response('test.html', {'mentors': test_list})


def robots(request):
    return render_to_response('robots.txt', content_type='text/plain')


def host(request):
    return_content = utils.is_login(request)
    # if return_content:
    #     return_content['is_login'] = True
    # else:
    #     return_content = dict()

    if request.method == 'GET':
        index_data = IndexAdmin.objects.all().first()
        return_content['index_data'] = index_data
        recommend = list()
        recommend.append(index_data.rec_mentor1)
        recommend.append(index_data.rec_mentor2)
        recommend.append(index_data.rec_mentor3)
        recommend.append(index_data.rec_mentor4)
        return_content['recommend'] = recommend
        notices = Notice.objects.order_by('-create_time').all()[:7]
        return_content['notices'] = notices
        return render_to_response('common/host.html',
                                  return_content)


def notices_list(request):
    return_content = utils.is_login(request)
    # if return_content:
    #     return_content['is_login'] = True
    # else:
    #     return_content = dict()
    if request.method == 'GET':
        page = request.GET.get('page')
        notices = Notice.objects.order_by('-create_time').all()
        paginator = Paginator(notices, 20)
        try:
            notices = paginator.page(page)
        except PageNotAnInteger:
            notices = paginator.page(1)
        except EmptyPage:
            notices = paginator.page(paginator.num_pages)

        return_content['notices'] = notices
        return render_to_response('common/notices_list.html',
                                  return_content)


def notice_detail(request):
    return_content = utils.is_login(request)
    # if return_content:
    #     return_content['is_login'] = True
    # else:
    #     return_content = dict()

    if request.method == 'GET':
        notice_id = request.GET.get('id')
        try:
            notice = Notice.objects.get(id=notice_id)
            return_content['notice'] = notice
        except Notice.DoesNotExist:
            raise Http404

        return render_to_response('common/notice_detail.html',
                                  return_content)


def login(request):
    body = {}
    if request.method == 'GET':
        refer_url = request.META.get('HTTP_REFERER', '')
        if 'fibar.cn' in refer_url and 'login' not in refer_url and 'register' not in refer_url:
            return render_to_response('common/login.html', {'refer': refer_url},
                                      context_instance=RequestContext(request))
        return render_to_response('common/login.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            body['status'] = "wrong forms"
            return HttpResponse(json.dumps(body))
        student_has = Student.objects.filter(account=request.POST.get('username'))
        if student_has.count() == 0:
            body['status'] = "用户名或者密码错误"
            return HttpResponse(json.dumps(body))
        if not student_has[0].check_password(request.POST.get('password')):
            body['status'] = "用户名或者密码错误"
            return HttpResponse(json.dumps(body))
        request.session['student'] = student_has[0].account
        body['status'] = 'success'
        return HttpResponse(json.dumps(body))


def login_by_qq(request):
    qq_client = APIClient(QQ_APP_ID, QQ_APP_KEY, redirect_uri='http://www.fibar.cn/qq_login_callback')
    url = qq_client.get_authorize_url(scopes=['get_user_info'])
    return HttpResponseRedirect(url)


def login_by_wechat(request):
    app_id = 'wx451b53fb7aec307e'
    encode_url = urllib.quote_plus('http://www.fibar.cn/wechat_login_callback')
    url = 'https://open.weixin.qq.com/connect/qrconnect?appid={0}&redirect_uri={1}&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect'.format(app_id, encode_url)
    return HttpResponseRedirect(url)


def login_by_wechat_inside(request):
    code = request.GET.get('code', None)
    if not code:
        current_url = '{0}{1}'.format(HOST, 'wechat_inside_login')
        encode_url = urllib.quote_plus(current_url)
        get_code_url = '''https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxed29f94c7e513349&redirect_uri={0}&response_type=code&scope=snsapi_userinfo#wechat_redirect'''.format(encode_url)
        return HttpResponseRedirect(get_code_url)
    else:
        req_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxed29f94c7e513349&secret=db22f19fa5b7f2da43feb4f5c4173bf9&code={0}&grant_type=authorization_code'.format(code)
        response = requests.get(req_url)
        json_res = json.loads(response.content)
        access_token = json_res.get('access_token')
        openid = json_res.get('openid')
        req_url = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN'.format(access_token, openid)
        response = requests.get(req_url)
        json_res = json.loads(response.content)
        union_id = json_res.get('unionid', None)
        if union_id:
                request.session['student'] = union_id
                wechat_user = Student.objects.filter(account=union_id)
                if not wechat_user.exists():
                    new_wechat_user = Student(account=union_id,
                                              nick=json_res.get('nickname', ''),
                                              avatar=json_res.get('headimgurl', ''),
                                              wx_union_id=union_id)
                    new_wechat_user.save()
                return HttpResponseRedirect('/search_teacher')
        return HttpResponse('授权失败,请重试')


def login_by_wechat_callback(request):
    app_id = 'wx451b53fb7aec307e'
    app_secret = 'd4624c36b6795d1d99dcf0547af5443d'
    code = request.GET.get('code', None)
    if code:
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(app_id, app_secret, code)
        result = requests.get(url).content
        json_data = json.loads(result)
        access_token = json_data.get('access_token', None)
        open_id = json_data.get('openid', None)
        if access_token and open_id:
            url = '''https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}'''.format(access_token, open_id)
            result = requests.get(url).content
            json_data = json.loads(result)
            nick_name = json_data.get('nickname', '')
            avatar = json_data.get('headimgurl', '')
            union_id = json_data.get('unionid', None)
            if union_id:
                request.session['student'] = union_id
                wechat_user = Student.objects.filter(account=union_id)
                if not wechat_user.exists():
                    new_wechat_user = Student(account=union_id,
                                              nick=nick_name,
                                              avatar=avatar,
                                              wx_union_id=union_id)
                    new_wechat_user.save()
                return HttpResponseRedirect('/search_teacher')
    return HttpResponse('授权失败,请重试')


def login_by_qq_callback(request):
    code = request.GET.get('code', None)
    qq_client = APIClient(QQ_APP_ID, QQ_APP_KEY, redirect_uri='http://www.fibar.cn/qq_login_callback')
    if code:
        qq_client.get_access_token(code=code, endpoint='token')
        open_id = qq_client.get_openid()
        ret = qq_client.get_user_info()
        user = Student.objects.filter(account=open_id)
        request.session['student'] = open_id
        if not user.exists():
            new_qq_user = Student(account=open_id,
                                  nick=ret.nickname,
                                  avatar=ret.figureurl_qq_1,
                                  qq_open_id=open_id)
            new_qq_user.save()
        #     return HttpResponseRedirect('/bind')
        # else:
        #     if user[0].account == user[0].qq_open_id:
        #         return HttpResponseRedirect('/bind')
        return HttpResponseRedirect('/search_teacher')
    else:
        return HttpResponse('授权失败,请重试')


def account_bind_page(request):
    token = request.session.get('student')
    user = Student.objects.filter(account=token)[0]
    return render_to_response({'nickname': user.nick,
                               'avatar': user.avatar}, 'common/bind.html')


def account_bind(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    student_has = Student.objects.filter(account=account)
    if student_has.count() == 0:
        body['status'] = "用户名或者密码错误"
        return HttpResponse(json.dumps(body))
    if not student_has[0].check_password(password):
        body['status'] = "用户名或者密码错误"
        return HttpResponse(json.dumps(body))
    token = request.session.get('student')
    student = student_has[0]
    bind_user_list = Student.objects.filter(wx_union_id=token) | Student.objects.filter(qq_open_id=token)
    if bind_user_list.exists():
        bind_user = bind_user_list[0]
        #change
        #delete
    request.session['student'] = student.account
    body['status'] = 'success'
    return HttpResponse((json.dumps(body)))


def logout(request):
    if request.method == 'GET':
        request.session.clear()
        return HttpResponseRedirect('/login')


def register(request):
    if request.method == 'GET':
        return render_to_response('common/register.html', context_instance=RequestContext(request))
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        print form
        if form.is_valid():
            pass
        else:
            return HttpResponse(json.dumps("wrong forms"))
        form_data = form.cleaned_data
        phone_verify = PhoneVerify.objects.filter(phone=form_data['phone'])
        user_has = Student.objects.filter(account=request.POST.get('username'))
        if not phone_verify.count() > 0:
            return HttpResponse(json.dumps(u"请先获取验证码"))
        if user_has.count() > 0:
            return HttpResponse(json.dumps(u"该用户已存在"))
        if phone_verify[0].is_expire():
            return HttpResponse(json.dumps(u"验证码已过期，请重新获取"))
        if not phone_verify[0].is_current(form_data['verify_code']):
            return HttpResponse(json.dumps(u"验证码错误"))

        new_user = Student()
        new_user.account = form_data['phone']
        new_user.nick = form_data['username']
        new_user.set_password(form_data['password'])
        new_user.avatar = create_random_avatar()
        new_user.save()
        phone_verify[0].delete()
        reg_mes = REG_MES % form_data['username'].encode('utf-8')
        create_new_message(reg_mes, new_user)
        return HttpResponse(json.dumps("success"))


@gzip_page
def search_teacher(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    # if return_content:
    #     # if return_content['login_type'] == 'teacher':
    #     #     return HttpResponseRedirect('/login')
    #     return_content['is_login'] = True
    # else:
    #     return_content = dict()

    heroes = Hero.objects.all()

    if request.method == 'GET':
        search = request.GET.get('search')
        teach_area = request.GET.get('teach_area')
        teach_position = request.GET.get('teach_position')
        teach_hero = request.GET.get('teach_hero')

        if teach_hero and not teach_hero == '' and not teach_hero == '0':
            hero_to_teach = Hero.objects.get(id=teach_hero)
        else:
            hero_to_teach = None
            teach_hero = ''

        mentors = Mentor.objects.all()
        if teach_area and not teach_area == '0':
            mentors = mentors.filter(Q(teach_area=teach_area) |
                                     Q(teach_area='0'))
        else:
            teach_area = '0'

        if teach_position and not teach_position == '0':
            mentors = mentors.filter(good_at__contains=teach_position)
            heroes = heroes.filter(hero_type__contains=teach_position)
        else:
            teach_position = '0'
            request.session['teach_position'] = '0'
        # 判断筛选位置是否改变，如果改变则重置筛选英雄
        if not request.session.get('teach_position') or not request.session['teach_position'] == teach_position:
            hero_to_teach = None
            teach_hero = ''

        request.session['teach_position'] = teach_position
        if hero_to_teach:
            mentors = mentors.filter(hero_list__id=teach_hero)

        if search and not search == '':
            for key, value in position_dic.items():
                if search == value:
                    mentors = mentors.filter(good_at__contains=key)
                    break

            for key, value in area_dic.items():
                if search == value:
                    mentors = mentors.filter(teach_area=key)
                    break

            mentors = mentors.filter(Q(nick__contains=search) |
                                     Q(hero_list__hero_name__contains=search))
        else:
            search = ''

        mentors = mentors.distinct()
        mentors = mentors.filter(disabled=False, type=1)
        mentors = mentors.order_by('status', '-priority', '-mark')
        for mentor in mentors:
            res = check_status(mentor)
            if not res:
                mentor.status = 2
                mentor.save()
        paginator = Paginator(mentors, 12)
        try:
            page_num = request.GET.get('page_num')
            mentors = paginator.page(page_num)
        except PageNotAnInteger:
            mentors = paginator.page(1)
        except EmptyPage:
            mentors = paginator.page(paginator.num_pages)
        return_content['mentors'] = mentors
        return_content['teach_area'] = teach_area
        return_content['teach_hero'] = hero_to_teach
        return_content['teach_position'] = teach_position
        return_content['search'] = search
        return_content['heroes'] = heroes
        return_content['referer'] = refer_url
        return render_to_response('common/search_teacher.html',
                                  return_content)


@gzip_page
def teacher_detail(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    # if return_content:
    #     # if return_content['login_type'] == 'teacher':
    #     #     return HttpResponseRedirect('/login')
    #     return_content['is_login'] = True
    # else:
    #     return_content = dict()

    if request.method == 'GET':
        mentor_id = request.GET.get('mentor_id')
        if not mentor_id:
            raise Http404
        try:
            mentor = Mentor.objects.get(id=mentor_id)
        except Mentor.DoesNotExist:
            raise Http404
        return_content['mentor_detail'] = mentor
        return_content['course_list'] = mentor.men_courses.all().order_by('create_time')
        if mentor.status == 2:
            last_orders = mentor.men_orders.filter(status=2).order_by('-create_time')
            if last_orders.count() > 0:
                last_time = last_orders[0].teach_end_time
                time_now = datetime.datetime.now(tz=get_current_timezone())
                if last_time <= time_now:
                    mentor.status = 1
                    mentor.save()
                return_content['teach_end_time'] = last_orders[0].teach_end_time
        comment_list = mentor.get_comment_list()
        total = comment_list.count()
        total_page = math.ceil(float(total) / 50.0)
        paginator = Paginator(comment_list, 50)
        page_num = 1
        comment = False
        try:
            page_num = int(request.GET.get('page'))
            comment_list = paginator.page(page_num)
            comment = True
        except PageNotAnInteger:
            comment_list = paginator.page(1)
        except EmptyPage:
            comment_list = []
        except:
            comment_list = paginator.page(page_num)
        first_page = 1
        last_page = int(total_page)
        page_list = [{'page': i} for i in range(1, int(total_page) + 1)]
        paginator_dict = {'first': first_page,
                          'last': last_page,
                          'current': page_num,
                          'page_list': page_list}
        return_content['paginator'] = paginator_dict
        return_content['comment_list'] = comment_list
        return_content['comment'] = comment
        return_content['referer'] = refer_url
        return render_to_response('common/teacher_detail.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def class_detail(request):
    course = CourseClass.objects.all()[0]
    lesson = Lesson.objects.all()[0]
    comment_list = lesson.get_comments()
    total = comment_list.count()
    total_page = math.ceil(float(total) / 50.0)
    paginator = Paginator(comment_list, 50)
    page_num = 1
    comment = False
    try:
        page_num = int(request.GET.get('page'))
        comment_list = paginator.page(page_num)
        comment = True
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = []
    except:
        comment_list = paginator.page(page_num)
    first_page = 1
    last_page = int(total_page)
    page_list = [{'page': i} for i in range(1, int(total_page) + 1)]
    paginator_dict = {'first': first_page,
                      'last': last_page,
                      'current': page_num,
                      'page_list': page_list}
    return render_to_response('common/class_detail.html', {'course': course,
                                                           'lesson': lesson,
                                                           'comment': comment,
                                                           'comment_count': total,
                                                           'comment_list': comment_list})


def about_us(request):
    return_content = utils.is_login(request)
    # if not return_content:
    #     return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/about_us.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def contact_us(request):
    return_content = utils.is_login(request)
    # if not return_content:
    #     return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/contact_us.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def laws(request):
    return_content = utils.is_login(request)
    # if not return_content:
    #     return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/laws.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def problems(request):
    return_content = utils.is_login(request)
    # if not return_content:
    #     return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/problems.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def service(request):
    return_content = utils.is_login(request)
    # if not return_content:
    #     return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/service.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def become_teacher(request):
    return_content = utils.is_login(request)
    # if not return_content:
    #     return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/become_teacher.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def update_header(request):
    return_content = utils.is_login(request)
    if not return_content['is_login']:
        raise Http404

    if return_content['login_type'] == 'student':
        user = return_content['active_user']
    elif return_content['login_type'] == 'teacher':
        user = return_content['mentor']

    if request.method == 'POST':
        form = UpdateHeaderForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            x1 = form_data['dataX1']
            y1 = form_data['dataY1']
            x2 = form_data['dataX2']
            y2 = form_data['dataY2']
            image = form_data['new_header']
            header = Image.open(image)
            region = (int(x1), int(y1), int(x2), int(y2))
            crop_img = header.crop(region)
            image_header = crop_img.resize((240, 240), Image.ANTIALIAS)
            image_header.save(BASE+'/static/img/user_avatar/' + str(user.id) + image.name)
            user.avatar = '/img/user_avatar/' + str(user.id) + image.name
            user.save()
            return HttpResponse(json.dumps('success'))
        else:
            return HttpResponse(json.dumps('wrong form'))


def forget_password(request):
    if request.method == 'GET':
        return render_to_response('common/forget_password.html',
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        verify_code = request.POST.get('verify_code')
        if not phone or not password or not verify_code:
            return HttpResponse(json.dumps('failed'))
        phone_verify = PhoneVerify.objects.filter(phone=phone)
        user_has = Student.objects.filter(account=phone)
        mentor_has = Mentor.objects.filter(account=phone)
        if not phone_verify.count() > 0:
            return HttpResponse(json.dumps(u"请先获取验证码"))
        if user_has.count() == 0 and mentor_has.count() == 0:
            return HttpResponse(json.dumps(u"该用户不存在"))
        if phone_verify[0].is_expire():
            return HttpResponse(json.dumps(u"验证码已过期，请重新获取"))

        if not phone_verify[0].is_current(verify_code):
            return HttpResponse(json.dumps(u"验证码错误"))
        if user_has.count() > 0:
            user = Student.objects.get(account=phone)
            user.set_password(password)
            user.save()
        elif mentor_has.count() > 0:
            mentor = Mentor.objects.get(account=phone)
            mentor.set_password(password)
            mentor.save()
        phone_verify[0].delete()

        return HttpResponse(json.dumps("success"))