# -*- coding: utf-8 -*-

import time
import os
import random
import string
import hashlib
import ujson
import datetime
import xlwt


from PIL import Image
from django.utils import timezone
from django.db.models import Q


from LYFAdmin.models import Admin, Order, Student

UPLOAD_PATH = os.path.dirname(os.path.dirname(__file__)) + '/static'

def upload_picture(pic_file, folder='hero/'):
    pic_name = str(int(time.time())) + str(random.randint(10000, 99999)) + '.png'
    pic_path = '/upload/' + folder + pic_name
    save_path = UPLOAD_PATH + pic_path
    img = Image.open(pic_file)
    img.save(save_path, "png")
    return pic_path, save_path


def datetime_to_string(datetimet, str_format='%Y-%m-%d %H:%M:%S'):
    if datetimet.tzinfo is None:
        return datetimet.strftime(str_format)
    time_str = datetimet.astimezone(timezone.get_current_timezone())
    return time_str.strftime(str_format)


def create_token(count=32):
    return string.join(
        random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba+=', count)).replace(" ", "")


def auth_admin(account, password):
    admin = Admin.objects.filter(account=account)
    if admin.exists():
        admin = admin[0]
        hash_passwd = hashlib.md5(password).hexdigest()
        if admin.password == hash_passwd:
            admin.token = create_token()
            admin.save()
            return admin
        else:
            return None
    else:
        return None


def encodejson(status, body):
    tmpjson={}
    tmpjson['status'] = status
    tmpjson['body'] = body
    return ujson.dumps(tmpjson)


def report_convert(status_type):
    n_str = ''
    if status_type == 1:
        n_str = '非本站交易（核查属实奖励50元）'
    elif status_type == 2:
        n_str = '未授课便完成订单'
    elif status_type == 3:
        n_str = '语音不雅'
    elif status_type == 4:
        n_str = '购买后无法联系'
    elif status_type == 5:
        n_str = '其他'
    return n_str


def hero_convert(type_str):
    nstr = u''
    for itm in type_str:
        if itm == '1':
            nstr += u'上单 '
        elif itm == '2':
            nstr += u'中单 '
        elif itm == '3':
            nstr += u'ADC '
        elif itm == '4':
            nstr += u'打野 '
        elif itm == '5':
            nstr += u'辅助 '
    return nstr


def area_convert(type_str):
    nstr = ''
    for itm in type_str:
        if itm == '0':
            nstr += '全区'
        elif itm == '1':
            nstr += '电信'
        elif itm == '2':
            nstr += '联通'
    return nstr


def order_status_convert(status_type):
    n_str = u''
    if status_type == 1:
        n_str = u'待确认'
    elif status_type == 2:
        n_str = u'已确认'
    elif status_type == 3:
        n_str = u'已完成'
    elif status_type == 4:
        n_str = u'已评价'
    elif status_type == 5:
        n_str = u'已撤单'
    elif status_type == 6:
        n_str = u'待支付'
    return n_str


def mentor_status_convert(status_type):
    n_str = ''
    if status_type == 3:
        n_str = '离线'
    elif status_type == 1:
        n_str = '接单'
    elif status_type == 2:
        n_str = '教学中'
    return n_str


def pay_type_convert(pay_type):
    n_str = ''
    if pay_type == 1:
        n_str = '在线支付'
    return n_str


def order_search(order_status, search_text):
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
                                                                              Q(belong__account__icontains=search_text) |
                                                                              Q(belong__nick__icontains=search_text) |
                                                                              Q(teach_by__account__icontains=search_text) |
                                                                              Q(teach_by__nick__icontains=search_text))
    return raw_order_list


def student_search(search_text):
    raw_stu_list = Student.objects.filter(Q(account__icontains=search_text) |
                                          Q(nick__icontains=search_text) |
                                          Q(qq__icontains=search_text) |
                                          Q(yy__icontains=search_text) |
                                          Q(phone__icontains=search_text) |
                                          Q(money__icontains=search_text))
    return raw_stu_list

def output_data(file_name, order_list):
    wb = xlwt.Workbook(encoding='utf-8')
    now_time = time.time()
    ws = wb.add_sheet(str(now_time))
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
    ws.write(0, 0, "订单号")
    ws.write(0, 1, "订单价格")
    ws.write(0, 2, "支付类型")
    ws.write(0, 3, "课程名称")
    ws.write(0, 4, "课程介绍")
    ws.write(0, 5, "学习区域")
    ws.write(0, 6, "学习位置")
    ws.write(0, 7, "学习英雄")
    ws.write(0, 8, "订单状态")
    ws.write(0, 9, "视频地址")
    ws.write(0, 10, "教学时间")
    ws.write(0, 11, "下单时间")
    ws.write(0, 12, "下单人")
    ws.write(0, 13, "教学导师")
    i = 1
    for item in order_list:
        print item.learn_type
        print type(item.learn_type)
        nstr = u''
        if item.learn_type == '1':
            nstr = u'上单 '
        elif item.learn_type == '2':
            nstr = u'中单 '
        elif item.learn_type == '3':
            nstr = u'ADC '
        elif item.learn_type == '4':
            nstr = u'打野 '
        elif item.learn_type == '5':
            nstr = u'辅助 '
        ws.write(i, 0, item.order_id, style0)
        ws.write(i, 1, item.order_price, style0)
        ws.write(i, 2, u"在线支付", style0)
        ws.write(i, 3, item.course_name)
        ws.write(i, 4, item.course_intro)
        ws.write(i, 5, item.learn_area)
        ws.write(i, 6, nstr)
        ws.write(i, 7, item.learn_hero)
        ws.write(i, 8, order_status_convert(item.status))
        ws.write(i, 9, item.teach_video)
        ws.write(i, 10, datetime_to_string(item.teach_start_time))
        ws.write(i, 11, datetime_to_string(item.create_time))
        ws.write(i, 12, item.belong.account)
        ws.write(i, 13, item.teach_by.account)
        i += 1
    output_path = "static/output/" + file_name
    wb.save(output_path)
    return '/output/' + file_name


def create_random_avatar():
    r_num = random.randint(1, 73)
    file_name = '/img/avatar/%i.png' % r_num
    return file_name


def check_start_time(mentor):
    orders = Order.objects.filter(teach_by=mentor, status=2).order_by('-teach_end_time')
    now_time = datetime.datetime.now(tz=timezone.get_current_timezone())
    if orders.exists():
        order = orders[0]
        last_time = order.teach_end_time
        if last_time == '' or last_time is None:
            return now_time
        time_interval = last_time - now_time
        time_zero = datetime.timedelta(minutes=0, seconds=0)
        if time_interval > time_zero:
            return last_time
        else:
            return now_time
    return now_time
