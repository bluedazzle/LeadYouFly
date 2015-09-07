# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
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
from LYFAdmin.utils import create_random_avatar
from LYFAdmin.message import REG_MES, create_new_message
from LYFAdmin.online_pay import create_alipay_order
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


def test(request):
    test_list = range(0, 5)
    return render_to_response('test.html', {'test_list': test_list})


def host(request):
    return_content = utils.is_login(request)
    if return_content:
        return_content['is_login'] = True
    else:
        return_content = dict()

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
    if return_content:
        return_content['is_login'] = True
    else:
        return_content = dict()
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
    if return_content:
        return_content['is_login'] = True
    else:
        return_content = dict()

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
    if request.method == 'GET':
        return render_to_response('common/login.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse(json.dumps("wrong forms"))
        student_has = Student.objects.filter(account=request.POST.get('username'))
        if student_has.count() == 0:
            return HttpResponse(json.dumps("用户名或者密码错误"))
        if not student_has[0].check_password(request.POST.get('password')):
            return HttpResponse(json.dumps("用户名或者密码错误"))
        request.session['student'] = student_has[0].account

        return HttpResponse(json.dumps("success"))


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


def search_teacher(request):
    return_content = utils.is_login(request)
    if return_content:
        # if return_content['login_type'] == 'teacher':
        #     return HttpResponseRedirect('/login')
        return_content['is_login'] = True
    else:
        return_content = dict()

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
            mentors = mentors.filter(teach_area=teach_area)
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
        mentors = mentors.order_by('-mark').order_by('-priority').order_by('status')
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
        return render_to_response('common/search_teacher.html',
                                  return_content)


def teacher_detail(request):
    return_content = utils.is_login(request)
    if return_content:
        # if return_content['login_type'] == 'teacher':
        #     return HttpResponseRedirect('/login')
        return_content['is_login'] = True
    else:
        return_content = dict()

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
            last_time = last_orders[0].teach_end_time
            time_now = datetime.datetime.now(tz=get_current_timezone())
            if last_time <= time_now:
                mentor.status = 1
                mentor.save()
            return_content['teach_end_time'] = last_orders[0].teach_end_time
        return render_to_response('common/teacher_detail.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def about_us(request):
    return_content = utils.is_login(request)
    if not return_content:
        return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/about_us.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def contact_us(request):
    return_content = utils.is_login(request)
    if not return_content:
        return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/contact_us.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def laws(request):
    return_content = utils.is_login(request)
    if not return_content:
        return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/laws.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def problems(request):
    return_content = utils.is_login(request)
    if not return_content:
        return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/problems.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def service(request):
    return_content = utils.is_login(request)
    if not return_content:
        return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/service.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def become_teacher(request):
    return_content = utils.is_login(request)
    if not return_content:
        return_content = dict()

    if request.method == 'GET':
        return render_to_response('common/become_teacher.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def update_header(request):
    return_content = utils.is_login(request)
    if return_content:
        return_content['is_login'] = True
    else:
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