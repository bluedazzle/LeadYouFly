# -*- coding: utf-8 -*-
import os
import time
import random
import hashlib
import ujson
import copy

from django.shortcuts import render
from django.shortcuts import render_to_response, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from PIL import Image
from dss.Serializer import serializer

from LYFAdmin.models import Hero, Mentor, IndexAdmin, Order, Course, Student, ChargeRecord, MoneyRecord, CashRecord, \
    Admin

from forms import MentorDetailContentForm
from decorator import login_require
from utils import upload_picture, datetime_to_string, auth_admin, hero_convert
from qn import upload_file_qn, list_file, QINIU_DOMAIN, VIDEO_CONVERT_PARAM, VIDEO_POSTER_PARAM, data_handle, \
    delete_data

# Create your views here.

# 管理登录
def admin_login(req):
    body = {}
    account = req.POST.get('username')
    password = req.POST.get('password')
    user = auth_admin(account, password)
    if user is None:
        return render_to_response('admin_login.html', {'fail': True})
    req.session['token'] = user.token
    return HttpResponseRedirect('/admin/index')


def admin_login_page(req):
    token = req.session.get('token', None)
    if token is not None:
        admin = Admin.objects.filter(token=token)
        if admin.exists():
            return HttpResponseRedirect('/admin/index')
    return render_to_response('admin_login.html', {'fail': False})


def admin_log_out(req):
    req.session.set_expiry(1)
    return render_to_response('admin_login.html', {'fail': False})


# 首页逻辑
@login_require
def admin_index(req):
    raw_index_admin = IndexAdmin.objects.all()[0]
    mentor_list = Mentor.objects.all()
    index_admin = serializer(raw_index_admin, deep=True)
    res, data_list = list_file(('index', 'poster'))
    index_video_list = []
    if res:
        for itm in data_list:
            items = {}
            items['name'] = unicode(itm['key']).split('poster')[0][0:-1]
            items['url'] = QINIU_DOMAIN + itm['key']
            index_video_list.append(copy.copy(items))
    return render_to_response('index_admin.html', {'index_admin': index_admin,
                                                   'mentor_list': mentor_list,
                                                   'video_list': index_video_list})


# 首页视频更改
@login_require
def admin_index_change_video(req):
    video_name = req.POST.get('video_radio', '')
    if video_name != '':
        res, data_list = list_file((video_name,))
        if res:
            index_admin = IndexAdmin.objects.all()[0]
            for itm in data_list:
                if 'poster' in itm['key']:
                    index_admin.video_poster = QINIU_DOMAIN + itm['key']
                else:
                    index_admin.index_video = QINIU_DOMAIN + itm['key']
            index_admin.save()
    return HttpResponseRedirect('/admin/index')


# 上传首页视频
@login_require
def admin_index_new_video(req):
    video_format = ['mp4', 'flv', 'avi', 'rmvb', 'webm', 'ogg']
    support_format = ['mp4', 'webm', 'ogg']
    video_data = req.FILES.get('new_video', None)
    if video_data is not None:
        file_name, ext_name = video_data.name.encode('utf-8').split('.')
        if ext_name in video_format:
            upload_name = file_name + '_' + str(int(time.time())) + '.' + ext_name
            res, sfile_name = upload_file_qn(video_data, upload_name, 'video_index')
            if res:
                poster_name = sfile_name.encode('utf-8').split('.')[0] + '_poster.jpg'
                res, info = data_handle(sfile_name, poster_name, VIDEO_POSTER_PARAM)
                if ext_name not in support_format:
                    new_name = sfile_name.encode('utf-8').split('.')[0] + '.mp4'
                    res, info = data_handle(sfile_name, new_name, VIDEO_CONVERT_PARAM)
                    delete_data(sfile_name.encode('utf-8'))
                    sfile_name = new_name
                index_admin = IndexAdmin.objects.all()[0]
                index_admin.index_video = QINIU_DOMAIN + sfile_name
                index_admin.video_poster = QINIU_DOMAIN + poster_name
                index_admin.save()
    return HttpResponseRedirect('/admin/index')


#更改推荐导师
@login_require
def admin_index_change_recommend(req):
    if req.method != 'POST':
        return Http404
    rec_id_1 = req.POST.get('rec_mentor_1')
    rec_id_2 = req.POST.get('rec_mentor_2')
    rec_id_3 = req.POST.get('rec_mentor_3')
    rec_id_4 = req.POST.get('rec_mentor_4')
    rec_mentor_1 = Mentor.objects.get(id=rec_id_1)
    rec_mentor_2 = Mentor.objects.get(id=rec_id_2)
    rec_mentor_3 = Mentor.objects.get(id=rec_id_3)
    rec_mentor_4 = Mentor.objects.get(id=rec_id_4)
    index_admin = IndexAdmin.objects.all()[0]
    index_admin.rec_mentor1 = rec_mentor_1
    index_admin.rec_mentor2 = rec_mentor_2
    index_admin.rec_mentor3 = rec_mentor_3
    index_admin.rec_mentor4 = rec_mentor_4
    index_admin.save()
    return HttpResponseRedirect('/admin/index')


#更改轮播图片
@login_require
def admin_index_change_picture(req):
    if req.method != 'POST':
        return Http404
    index_pic_1 = req.FILES.get('pic_choice_1', None)
    index_pic_2 = req.FILES.get('pic_choice_2', None)
    index_pic_3 = req.FILES.get('pic_choice_3', None)
    index_admin = IndexAdmin.objects.all()[0]
    if index_pic_1 is not None:
        p1_path, full_path = upload_picture(index_pic_1, 'img/')
        index_admin.index_pic1 = p1_path
    if index_pic_2 is not None:
        p2_path, full_path = upload_picture(index_pic_2, 'img/')
        index_admin.index_pic2 = p2_path
    if index_pic_3 is not None:
        p3_path, full_path = upload_picture(index_pic_3, 'img/')
        index_admin.index_pic3 = p3_path
    index_admin.save()
    return HttpResponseRedirect('/admin/index')


#网站管理
@login_require
def admin_website(req):
    hero_list = Hero.objects.all()
    for itm in hero_list:
        itm.hero_type = hero_convert(itm.hero_type)
    return render_to_response('website_admin.html', {'hero_list': hero_list})


#删除英雄
def admin_website_del_hero(req):
    hid = req.GET.get('hid')
    hero = get_object_or_404(Hero, id=hid)
    hero.delete()
    return HttpResponseRedirect('/admin/website')


#添加英雄
@login_require
def admin_website_new_hero(req):
    if req.method != 'POST':
        return Http404
    hero_pic = req.FILES.get('picture')
    hero_name = req.POST.get('hero_name')
    hero_type = req.POST.getlist('hero_type')
    h_type = ''
    for itm in hero_type:
        h_type += itm
    if hero_type == '':
        h_type = '1'
    background = req.FILES.get('background')
    pic_path, full_path = upload_picture(hero_pic)
    back_path, full_path = upload_picture(background, 'hback/')
    new_hero = Hero(hero_name=hero_name,
                    hero_picture=pic_path,
                    hero_background=back_path,
                    hero_type=h_type)
    new_hero.save()
    return HttpResponseRedirect('/admin/website')


#订单管理
@login_require
def admin_order(req):
    raw_order_list = Order.objects.all().order_by('-create_time')
    order_list = serializer(raw_order_list, deep=True, datetime_format='string')
    return render_to_response('order_admin.html', {'order_list': order_list,
                                                   'select_code': 0})


@login_require
def admin_order_search(req):
    if req.method != 'POST':
        return Http404
    search_text = req.POST.get('search_text', '')
    order_status = int(req.POST.get('order_status', 0))
    if search_text == '' or search_text is None:
        if order_status == 0:
            raw_order_list = Order.objects.all()
        else:
            raw_order_list = Order.objects.filter(status=order_status)
    else:
        if order_status == 0:
            raw_order_list = Order.objects.filter(Q(order_price__icontains=search_text) |
                                                  Q(course_name__icontains=search_text) |
                                                  Q(belong__account__icontains=search_text) |
                                                  Q(belong__nick__icontains=search_text) |
                                                  Q(teach_by__account__icontains=search_text) |
                                                  Q(teach_by__nick__icontains=search_text))
        else:
            raw_order_list = Order.objects.filter(status=order_status).filter(Q(order_price__icontains=search_text) |
                                                                              Q(course_name__icontains=search_text) |
                                                                              Q(
                                                                                  belong__account__icontains=search_text) |
                                                                              Q(belong__nick__icontains=search_text) |
                                                                              Q(
                                                                                  teach_by__account__icontains=search_text) |
                                                                              Q(teach_by__nick__icontains=search_text))
    order_list = serializer(raw_order_list, deep=True)
    return render_to_response('order_admin.html', {'order_list': order_list,
                                                   'select_code': order_status})


#导师管理
@login_require
def admin_mentor(req):
    raw_mentor_list = Mentor.objects.all().order_by('-create_time')
    mentor_list = serializer(raw_mentor_list, datetime_format='string')
    for i, mentor in enumerate(raw_mentor_list):
        mentor_list[i]['total_orders'] = mentor.men_orders.all().count()
    return render_to_response('mentor_admin.html', {'mentor_list': mentor_list})


#添加导师
@login_require
def admin_mentor_new_mentor(req):
    if req.method != 'POST':
        return Http404
    account = req.POST.get('mentor_account', '')
    passwd = req.POST.get('mentor_passwd', '')
    nick = req.POST.get('mentor_nick', '')
    if account == '' or passwd == '':
        return Http404
    mentor = Mentor.objects.filter(account=account)
    print mentor.count()
    if mentor.exists():
        return Http404
    hash_pass = hashlib.md5(passwd).hexdigest()
    new_mentor = Mentor(account=account,
                        password=hash_pass,
                        nick=nick)
    new_mentor.save()
    return HttpResponseRedirect('/admin/mentor')


#导师改变介绍视频
def admin_mentor_change_video(req, mid):
    video_name = req.POST.get('video_radio', '')
    if video_name != '':
        res, data_list = list_file((video_name,))
        if res:
            mentor = get_object_or_404(Mentor, id=mid)
            for itm in data_list:
                if 'poster' in itm['key']:
                    mentor.video_poster = QINIU_DOMAIN + itm['key']
                else:
                    mentor.intro_video = QINIU_DOMAIN + itm['key']
            mentor.save()
    new_url = '/admin/mentor/detail/' + str(mid) + '/'
    return HttpResponseRedirect(new_url)


#导师添加新视频
def admin_mentor_new_video(req, mid):
    video_format = ['mp4', 'flv', 'avi', 'rmvb', 'webm', 'ogg']
    support_format = ['mp4', 'webm', 'ogg']
    video_data = req.FILES.get('new_video', None)
    mentor = get_object_or_404(Mentor, id=mid)
    if video_data is not None:
        file_name, ext_name = video_data.name.encode('utf-8').split('.')
        if ext_name in video_format:
            upload_name = file_name + '_' + str(int(time.time())) + '.' + ext_name
            sign = 'video_mentor_' + str(mid)
            res, sfile_name = upload_file_qn(video_data, upload_name, sign)
            if res:
                poster_name = sfile_name.encode('utf-8').split('.')[0] + '_poster.jpg'
                res, info = data_handle(sfile_name, poster_name, VIDEO_POSTER_PARAM)
                if ext_name not in support_format:
                    new_name = sfile_name.encode('utf-8').split('.')[0] + '.mp4'
                    res, info = data_handle(sfile_name, new_name, VIDEO_CONVERT_PARAM)
                    delete_data(sfile_name.encode('utf-8'))
                    sfile_name = new_name
                mentor.intro_video = QINIU_DOMAIN + sfile_name
                mentor.video_poster = QINIU_DOMAIN + poster_name
                mentor.save()
    new_url = '/admin/mentor/detail/' + str(mid) + '/'
    return HttpResponseRedirect(new_url)


#导师课程价格变更
@login_require
def admin_mentor_change_price(req, mid, cid):
    mentor = get_object_or_404(Mentor, id=mid)
    course = get_object_or_404(Course, id=cid)
    if course.belong != mentor:
        return Http404
    new_price = float(req.GET.get('new_price'))
    course.price = new_price
    print new_price
    course.save()
    re_url = '/admin/mentor/detail/' + mid + '/'
    return HttpResponseRedirect(re_url)


#导师英雄池删除英雄
@login_require
def admin_mentor_del_hero(req, mid, hid):
    mentor = get_object_or_404(Mentor, id=mid)
    hero = get_object_or_404(Hero, id=hid)
    hero_list = mentor.hero_list.all()
    if hero in hero_list:
        mentor.hero_list.remove(hero)
    re_url = '/admin/mentor/detail/' + mid + '/'
    return HttpResponseRedirect(re_url)


#导师英雄池添加英雄
@login_require
def admin_mentor_add_hero(req, mid):
    new_hero_id = req.POST.get('new_hero_select', '')
    hero = get_object_or_404(Hero, id=new_hero_id)
    mentor = get_object_or_404(Mentor, id=mid)
    hero_list = mentor.hero_list.all()
    if hero not in hero_list:
        mentor.hero_list.add(hero)
        mentor.save()
    re_url = '/admin/mentor/detail/' + mid + '/'
    return HttpResponseRedirect(re_url)


#导师详情更新
@login_require
def admin_mentor_update_detail(req, mid):
    form = MentorDetailContentForm(req.POST)
    if form.is_valid():
        update_content = form.cleaned_data['Mentor_Detail']
        mentor = get_object_or_404(Mentor, id=mid)
        mentor.intro_detail = update_content
        mentor.save()
    re_url = '/admin/mentor/detail/' + mid + '/'
    return HttpResponseRedirect(re_url)


@login_require
def admin_student(req):
    raw_stu_list = Student.objects.all().order_by('-create_time')
    stu_list = serializer(raw_stu_list, datetime_format='string')
    for i, stu in enumerate(raw_stu_list):
        total_expense = 0.0
        last_time = ''
        order_list = stu.stu_orders.all().order_by('-create_time')
        if order_list.exists():
            last_time = datetime_to_string(order_list[0].create_time)
            for itm in order_list:
                total_expense += float(itm.order_price)
        stu_list[i]['total_expense'] = total_expense
        stu_list[i]['last_order_time'] = last_time
    return render_to_response('student_admin.html', {'stu_list': stu_list})


@login_require
def admin_audit(req):
    order_list = Order.objects.filter(if_upload_video=True, video_audit=False)
    order_list = serializer(order_list, deep=True, datetime_format='string')
    return render_to_response('audit_admin.html', {'video_list': order_list})


@login_require
def admin_pay(req):
    mentor_list = Mentor.objects.all().order_by('-create_time')
    mentor_list = serializer(mentor_list, datetime_format='string')
    return render_to_response('pay_mentor_admin.html', {'mentor_list': mentor_list})


#解冻导师
@login_require
def admin_pay_thaw(req, mid):
    mentor = get_object_or_404(Mentor, id=mid)
    mentor.freeze = False
    mentor.save()
    return HttpResponseRedirect('/admin/pay/')


#冻结导师
@login_require
def admin_pay_freeze(req, mid):
    mentor = get_object_or_404(Mentor, id=mid)
    mentor.freeze = True
    mentor.save()
    return HttpResponseRedirect('/admin/pay/')


#学员充值纪录
@login_require
def admin_pay_stu_rec(req):
    charge_list = ChargeRecord.objects.all().order_by('-create_time')
    charge_list = serializer(charge_list, datetime_format='string', deep=True)
    return render_to_response('pay_stu_rec.html', {'charge_list': charge_list})


#导师收支纪录
@login_require
def admin_pay_mentor_rec(req):
    money_rec_list = MoneyRecord.objects.all().order_by('-create_time')
    money_rec_list = serializer(money_rec_list, datetime_format='string', deep=True)
    return render_to_response('pay_mentor_rec.html', {'record_list': money_rec_list})


#同意提款
@login_require
def admin_pay_agree_cash(req, cid):
    record = get_object_or_404(CashRecord, id=cid)
    record.manage = True
    record.agree = True
    record.save()
    return HttpResponseRedirect('/admin/pay/cash/')


#驳回提款
@login_require
def admin_pay_rejected_cash(req, cid):
    record = get_object_or_404(CashRecord, id=cid)
    record.manage = True
    record.agree = False
    record.save()
    return HttpResponseRedirect('/admin/pay/cash/')


#导师提现请求
@login_require
def admin_pay_cash(req):
    cash_list = CashRecord.objects.all().order_by('-create_time').order_by('manage')
    cash_list = serializer(cash_list, datetime_format='string', deep=True)
    return render_to_response('pay_cash.html', {'cash_record': cash_list})


#导师详情
@login_require
def admin_mentor_detail(req, mid):
    mentor = get_object_or_404(Mentor, id=mid)
    hero_list = mentor.hero_list.all()
    hero_pool = Hero.objects.all()
    course_list = mentor.men_courses.all()
    sign = 'video_mentor_' + str(mid)
    res, data_list = list_file((sign, 'poster', ))
    video_list = []
    for itm in data_list:
        items = {}
        items['name'] = unicode(itm['key']).split('poster')[0][0:-1]
        items['url'] = QINIU_DOMAIN + itm['key']
        video_list.append(copy.copy(items))
    form = MentorDetailContentForm(initial={'Mentor_Detail': mentor.intro_detail})
    return render_to_response('mentor_detail_admin.html', {'form': form,
                                                           'video_list': video_list,
                                                           'hero_list': hero_list,
                                                           'mentor': mentor,
                                                           'course_list': course_list,
                                                           'hero_pool': hero_pool})


#导师信息
@login_require
def admin_mentor_info(req, mid):
    mentor = get_object_or_404(Mentor, id=mid)
    mentor = serializer(mentor, datetime_format='string')
    return render_to_response('mentor_info_admin.html', {'mentor': mentor})


#导师订单
@login_require
def admin_mentor_order(req, mid):
    mentor = get_object_or_404(Mentor, id=mid)
    mentor_order_list = mentor.men_orders.all()
    mentor_order_list = serializer(mentor_order_list, deep=True)
    return render_to_response('mentor_order_admin.html', {'order_list': mentor_order_list,
                                                          'mentor': mentor})


#学员信息
@login_require
def admin_student_info(req, sid):
    student = get_object_or_404(Student, id=sid)
    order_list = student.stu_orders.all()
    total_expense = 0.0
    for itm in order_list:
        total_expense += float(itm.order_price)
    student = serializer(student)
    student['total_expense'] = total_expense
    return render_to_response('student_info_admin.html', {'student': student})


#学员订单
@login_require
def admin_student_order(req, sid):
    student = get_object_or_404(Student, id=sid)
    order_list = student.stu_orders.all().order_by('-create_time')
    order_list = serializer(order_list, deep=True, datetime_format='string')
    return render_to_response('student_order_admin.html', {'student': student,
                                                           'order_list': order_list})



