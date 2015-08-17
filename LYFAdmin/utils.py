# -*- coding: utf-8 -*-

import time
import os
import random
import string
import hashlib
import ujson
import xlwt


from PIL import Image
from django.utils import timezone
from django.db.models import Q


from LYFAdmin.models import Admin, Order

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


def hero_convert(type_str):
    nstr = ''
    for itm in type_str:
        if itm == '1':
            nstr += '上单 '
        elif itm == '2':
            nstr += '中单 '
        elif itm == '3':
            nstr += 'ADC'
        elif itm == '4':
            nstr += '打野 '
        elif itm == '5':
            nstr += '辅助 '
    return nstr


def order_status_convert(status_type):
    n_str = ''
    if status_type == 1:
        n_str = '待确认'
    elif status_type == 2:
        n_str = '已确认'
    elif status_type == 3:
        n_str = '已完成'
    elif status_type == 4:
        n_str = '已评价'
    elif status_type == 5:
        n_str = '已撤单'
    return n_str


def mentor_status_convert(status_type):
    n_str = ''
    if status_type == 0:
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
                                                                              Q(
                                                                                  belong__account__icontains=search_text) |
                                                                              Q(belong__nick__icontains=search_text) |
                                                                              Q(
                                                                                  teach_by__account__icontains=search_text) |
                                                                              Q(teach_by__nick__icontains=search_text))
    return raw_order_list


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
        ws.write(i, 0, item.order_id, style0)
        ws.write(i, 1, item.order_price, style0)
        ws.write(i, 2, pay_type_convert(item.pay_type), style0)
        ws.write(i, 3, item.course_name)
        ws.write(i, 4, item.course_intro)
        ws.write(i, 5, item.learn_area)
        ws.write(i, 6, hero_convert(str(item.learn_type)))
        ws.write(i, 7, item.learn_hero)
        ws.write(i, 8, order_status_convert(item.status))
        ws.write(i, 9, item.teach_video)
        ws.write(i, 10, datetime_to_string(item.teach_time))
        ws.write(i, 11, datetime_to_string(item.create_time))
        ws.write(i, 12, item.belong.account)
        ws.write(i, 13, item.teach_by.account)
        i += 1
    output_path = "static/output/" + file_name
    wb.save(output_path)
    return '/output/' + file_name