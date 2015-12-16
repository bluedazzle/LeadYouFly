# -*- coding: utf-8 -*-
import urllib
from django.shortcuts import get_object_or_404
from dss import Serializer
from LYFAdmin.message import EXP_MES, LVLUP_MES
from LYFAdmin.order_operation import create_order_id
from LYFAdmin.utils import area_convert, encodejson, datetime_to_string
from LYFAdmin.wechat_pay import build_form_by_params
from LeadYouFly.settings import HOST
from views import *
from weichat.models import Promotion, Reward
from weichat.wechat_service import WechatService
import time
from weichat.wtf import send_message

exp_dic = {
    1: 0,
    2: 10,
    3: 40,
    4: 70,
    5: 100,
    6: 150,
    7: 300,
    8: 600,
    9: 1000,
    10: 1500,
    11: 2000,
    12: 3000,
    13: 5000,
    14: 8000,
    15: 15000,
    16: 100000000
}


def user_message(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404
    return_content['is_login'] = True
    message_list = Message.objects.filter(belong=return_content['active_user']) | Message.objects.filter(send_all=True)
    message_list = message_list.order_by('-create_time')
    # test_list = range(0, 6)
    # return_content['test_list'] = test_list
    return_content['message_list'] = message_list
    return render_to_response('user/message.html',
                              return_content,
                              context_instance=RequestContext(request))


def complete_mes(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    return_content['referer'] = refer_url
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404
    student_active = return_content['active_user']

    if request.method == 'GET':
        return render_to_response('user/complete_mes.html',
                                  return_content,
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = CompleteInfoForm(request.POST)
        next_page = request.GET.get('next_page', None)
        if form.is_valid():
            form_data = form.cleaned_data
            student_active.qq = form_data['qq']
            student_active.phone = form_data['phone']
            student_active.save()
            return HttpResponse(json.dumps({'status': 'success',
                                            'next_page': next_page}))

        return HttpResponse(json.dumps({'status': 'wrong form'}))


def my_orders(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    return_content['referer'] = refer_url
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        orders = Order.objects.order_by('-create_time').filter(belong=return_content['active_user'])
        orders_first = list(orders.filter(status=6))
        orders_last = list(orders.exclude(status=6).order_by('status'))
        orders = orders_first + orders_last
        paginator = Paginator(orders, 10)
        try:
            page_num = request.GET.get('page_num')
            orders = paginator.page(page_num)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        return_content['orders'] = orders
        return render_to_response('user/my_order.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def appraise_order(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    return_content['referer'] = refer_url
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        try:
            order = Order.objects.get(order_id=order_id,
                                      status=3)
            return_content['order'] = order
            return render_to_response('user/appraise.html',
                                      return_content,
                                      context_instance=RequestContext(request))
        except Order.DoesNotExist:
            raise Http404
        except:
            raise Http404

    if request.method == 'POST':
        form = AppraiseOrder(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
        else:
            return HttpResponse(json.dumps("wrong form"))
        try:
            order = Order.objects.get(order_id=form_data['order_id'],
                                      belong=return_content['active_user'],
                                      status=3)
            order.status = 4
            new_comment = Comment()
            new_comment.mark = float(form_data['stars'])
            new_comment.content = form_data['content']
            new_comment.comment_mentor = order.teach_by
            new_comment.comment_by = return_content['active_user']
            new_comment.save()
            order.comment = new_comment
            order.save()
            mentor = order.teach_by
            all_order_grades = 0
            for order in mentor.men_orders.filter(status=4):
                if order.comment:
                    all_order_grades += order.comment.mark * 2
            all_order_count = mentor.men_orders.filter(status=4).count()
            last_grade = (all_order_grades + 90) / (all_order_count + 10)
            mentor.mark = round(last_grade, 1)
            mentor.save()
            user = return_content['active_user']
            user.exp += int(order.order_price)
            for key, value in exp_dic.items():
                if user.exp >= value and user.rank < key:
                    user.rank = key
                    lvl_mes = LVLUP_MES % key
                    create_new_message(lvl_mes, user)
            user.save()
        except Order.DoesNotExist:
            raise Http404
        except:
            return HttpResponse(json.dumps("wrong request"))
        coment_mes = EXP_MES % (str(int(order.order_price)), str(user.rank),
                                str(exp_dic[int(user.rank) + 1] - int(user.exp)))
        create_new_message(coment_mes, user)
        return HttpResponse(json.dumps("success"))


def my_follow_mentors(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    return_content['referer'] = refer_url
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        return render_to_response('user/follow_mentor.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def follow_mentor(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    return_content['referer'] = refer_url
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        mentor_id = request.GET.get('mentor_id')
        student_active = return_content['active_user']
        try:
            mentor = Mentor.objects.get(id=mentor_id)
            if student_active.follow.filter(id=mentor_id).count() == 0:
                student_active.follow.add(mentor)
            else:
                raise Http404
        except Mentor.DoesNotExist:
            raise Http404

        return HttpResponse(json.dumps(mentor_id))


def cancel_follow(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        mentor_id = request.GET.get('mentor_id')
        student_active = return_content['active_user']
        try:
            mentor = Mentor.objects.get(id=mentor_id)
            if not student_active.follow.filter(id=mentor_id).count() == 0:
                student_active.follow.remove(mentor)
            else:
                raise Http404
        except Mentor.DoesNotExist:
            raise Http404

        return HttpResponse(json.dumps(mentor_id))


def confirm_order(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    if return_content and return_content['login_type'] == 'student':
        return_content['is_login'] = True
    else:
        return HttpResponseRedirect('/login')
    return_content['referer'] = refer_url
    student = return_content['active_user']
    # if student.phone == '' or student.qq == '':
    #     next_page = request.get_full_path()
    #     return HttpResponseRedirect('/user/complete_mes?next_page=%s' % next_page)
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        # if student.wx_open_id == '':
        code = request.GET.get('code', False)
        is_wx = True if str(request.GET.get('wechat', False)) == '1' else False
        if is_wx:
            if not code:
                current_url = '{0}{1}'.format(HOST, request.get_full_path()[1:])
                encode_url = urllib.quote_plus(current_url)
                get_code_url = '''https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxed29f94c7e513349&redirect_uri={0}&response_type=code&scope=snsapi_base#wechat_redirect'''.format(encode_url)
                return HttpResponseRedirect(get_code_url)
            else:
                wx = WechatService()
                data = wx.get_user_info_by_code(code)
                open_id = data['openid']
                union_id = data['unionid']
                student.wx_open_id = open_id
                student.wx_union_id = union_id
                student.save()
        if not course_id:
            raise Http404
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise Http404
        mentor = course.belong
        if mentor.status == 3:
            return HttpResponseRedirect('/mentor_detail?mentor_id=' + mentor.id)
        return_content['hero_list'] = mentor.hero_list.all()
        return_content['course'] = course
        return render_to_response('common/confirm_order.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def big_wheel(req):
    code = req.GET.get('code', False)
    if not code:
        current_url = '{0}{1}'.format(HOST, req.get_full_path()[1:])
        encode_url = urllib.quote_plus(current_url)
        get_code_url = '''https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxed29f94c7e513349&redirect_uri={0}&response_type=code&scope=snsapi_base#wechat_redirect'''.format(encode_url)
        return HttpResponseRedirect(get_code_url)
    else:
        wx = WechatService()
        data = wx.get_user_info_by_code(code)
        open_id = data.get('openid', None)
        if open_id is None:
            return HttpResponseRedirect('/luckyDraw')
        promotion_list = Promotion.objects.filter(open_id=open_id)
        if promotion_list.exists():
            promotion = promotion_list[0]
        else:
            promotion = wx.get_promotion_info(open_id)
        reward_list = Reward.objects.all().order_by('-create_time')
        content = '''[{"id":0,"prize":"大奖降临：大奖降临:雷蛇 Taipan 太攀皇蛇游戏鼠标","v":0.0001},{"id":1,"prize":"一等奖：LOL1000点券点卡","v":0.001},{"id":2,"prize":"二等奖：LOL500点券点卡","v":0.002},{"id":3,"prize":"三等奖：LOL双倍经验卡一日","v":1.0},{"id":4,"prize":"幸运奖：LOL100点券点卡","v":90.0}]'''
        if not promotion.play:
            return render_to_response('user/bigwheel.html', {'status': 1,
                                                             'content': content,
                                                             'open_id': promotion.open_id,
                                                             'reward_list': reward_list})
        else:
            return render_to_response('user/bigwheel.html', {'status': 0,
                                                             'content': content,
                                                             'open_id': promotion.open_id,
                                                             'reward_list': reward_list})


def get_reward_result(req):
    open_id = str(req.GET.get('openid', False))
    rtype = int(req.GET.get('rtype', -1))
    content = req.GET.get('content', '')
    if open_id:
        promotion = get_object_or_404(Promotion, open_id=open_id)
        if promotion.play is True:
            return HttpResponse('fail')
        promotion.play = True
        promotion.save()
        if rtype != -1:
            new_reward = Reward(user=promotion,
                                reward=content)
            new_reward.save()
            message = '''恭喜你获得{0}，

        请回复【qq+QQ号】例如:

        qq540249125（注意只能是英文字母qq+QQ账号哦），

        我们将在24小时内将自动为你充值。

        如24小时未收到点券，请电话010-53355989'''.format(content)
            print open_id
            res = send_message(open_id, message)
            return HttpResponse(res)
    return HttpResponse('false')


def get_reward_list(req):
    reward_list = Reward.objects.all().order_by('-create_time')
    data = []
    for itm in reward_list:
        body = {}
        body['奖品'] = itm.reward
        body['微信昵称'] = itm.user.nick
        body['QQ'] = itm.user.qq
        body['时间'] = datetime_to_string(itm.create_time)
        data.append(body)
    return HttpResponse(json.dumps(data, ensure_ascii=False))


def repay_order(req):
    return_content = utils.is_login(req)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404
    order_id =req.GET.get('order_id', None)
    if order_id:
        order = get_object_or_404(Order, order_id=order_id)
        pay_url = create_alipay_order(order_id, order.course_name, order.order_price)
        return HttpResponseRedirect(pay_url)



def create_order(req):
    body = {}
    return_content = utils.is_login(req)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404
    cid = req.POST.get('course_id', None)
    qq = req.POST.get('qq', None)
    phone = req.POST.get('phone', None)
    channel = req.POST.get('channel', None)
    course = get_object_or_404(Course, id=cid)
    mentor = course.belong
    if mentor.status == 3:
        url = '/mentor_detail?mentor_id={0}'.format(mentor.id)
        body['redirect_url'] = url
        body['err_msg'] = u'教练休息中，无法下单'
        return HttpResponse(encodejson(2, body), content_type='application/json')
    student = return_content['active_user']
    student.phone = phone
    student.qq = qq
    student.save()
    order_id = create_order_id(student.id, mentor.id)
    if channel == 'wechat':
        params = {'body': course.name,
                  'out_trade_no': order_id,
                  'spbill_create_ip': req.META.get('REMOTE_ADDR', '127.0.0.1'),
                  'openid': student.wx_open_id,
                  'total_fee': int(float(course.price) * 100)}
        repay_data = build_form_by_params(params)
        body['data'] = repay_data
    else:
        pay_url = create_alipay_order(order_id, course.name, course.price)
        body['data'] = pay_url
    # now_time = datetime.datetime.now(tz=get_current_timezone())
    # pre_time = now_time.replace(hour=0, minute=0, second=0)
    # order_num = Order.objects.filter(create_time__range=(pre_time, now_time), status=2, teach_by=mentor).count()
    # wait_hours = order_num * 1.5
    # delta_hours = datetime.timedelta(hours=wait_hours)
    # wait_time = now_time + delta_hours
    learn_area = area_convert(str(mentor.teach_area))
    start_time = datetime.datetime(year=1970, month=1, day=1, tzinfo=get_current_timezone())
    new_order = Order(order_id=order_id,
                      order_price=course.price,
                      course_name=course.name,
                      course_intro=course.course_info,
                      learn_area=learn_area,
                      learn_hero='',
                      learn_type='',
                      belong=student,
                      teach_end_time=start_time,
                      teach_start_time=start_time,
                      teach_by=mentor)
    new_order.save()
    body['channel'] = channel
    return HttpResponse(encodejson(1, body), content_type='application/json')


def complain(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    return_content['referer'] = refer_url
    if return_content and return_content['login_type'] == 'student':
        return_content['is_login'] = True
    else:
        return HttpResponseRedirect('/login')

    if request.method == 'GET':
        return render_to_response('user/complain.html',
                                  return_content,
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = ComplainForm(request.POST)
        print request.POST
        if form.is_valid():
            form_data = form.cleaned_data
            new_report = Report()
            new_report.reporter = return_content['active_user']
            new_report.name = form_data['name']
            new_report.phone = form_data['phone']
            new_report.qq = form_data['qq']
            new_report.reported = form_data['mentor_name']
            new_report.content = form_data['complain_content']
            new_report.type = int(form_data['check_id'][-1])
            image_list = json.loads(form_data['image_list'])
            for i in range(0, len(image_list)):
                if i == 0:
                    new_report.pic1 = image_list[i]
                if i == 1:
                    new_report.pic2 = image_list[i]
                if i == 2:
                    new_report.pic3 = image_list[i]
                if i == 3:
                    new_report.pic4 = image_list[i]

            new_report.save()
            return HttpResponse(json.dumps("success"))
        else:
            return HttpResponse(json.dumps("failed"))


def upload_complain_pic(request):
    return_content = utils.is_login(request)
    if return_content and return_content['login_type'] == 'student':
        return_content['is_login'] = True
    else:
        return HttpResponse(json.dumps("failed"))

    if request.method == 'POST':
        upload_pic = request.FILES.get('upload_pic', None)
        number_pic = request.POST.get('number')
        if number_pic and int(number_pic) <= 4:
            file_name = str(int(time.time())) + upload_pic.name
            file_full_path = BASE + '/static/tmp/' + file_name
            Image.open(upload_pic).save(file_full_path)
            return HttpResponse(json.dumps('/tmp/' + file_name))
        else:
            return HttpResponse(json.dumps("failed"))


def security_center(request):
    refer_url = request.META.get('HTTP_REFERER', '')
    return_content = utils.is_login(request)
    return_content['referer'] = refer_url
    if return_content and return_content['login_type'] == 'student':
        return_content['is_login'] = True
    else:
        return HttpResponseRedirect('/login')

    if request.method == 'GET':
        return render_to_response('user/security_center.html',
                                  return_content,
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user_active = return_content['active_user']
            if user_active.check_password(form_data['origin_password']) and form_data['new_password'] == \
                    form_data['password_again']:
                user_active.set_password(form_data['new_password'])
                user_active.save()
                request.session.clear()
                return HttpResponse(json.dumps('success'))
            else:
                return HttpResponse(json.dumps('failed'))
        else:
            return HttpResponse(json.dumps('wrong form'))


def cancel_order(request):
    return_content = utils.is_login(request)
    if return_content and return_content['login_type'] == 'student':
        return_content['is_login'] = True
    else:
        return HttpResponseRedirect('/login')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id, status=6)
            order.status = 5
            order.save()
            return HttpResponse(json.dumps('success'))
        except Order.DoesNotExist:
            return HttpResponse(json.dumps('no such order'))