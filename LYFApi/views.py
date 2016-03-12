# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from LYFAdmin.models import Student, Order
# Create your views here.

import json

from LYFAdmin.utils import datetime_to_string
from LeadYouFly.settings import SEO_HOST


def encodejson(status, body):
    tmpjson = {}
    tmpjson['status'] = status
    tmpjson['body'] = body
    return json.dumps(tmpjson)


@csrf_exempt
def login(req):
    body = {}
    username = req.POST.get('username', None)
    password = req.POST.get('password', None)
    user_list = Student.objects.filter(account=username)
    if user_list.exists():
        user = user_list[0]
        if user.check_password(password):
            body['username'] = username
            body['nick'] = user.nick
            body['mail'] = '{0}@qq.com'.format(user.qq)
            body['avatar'] = '{0}{1}'.format(SEO_HOST, user.avatar)
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['message'] = '密码错误'
            return HttpResponse(encodejson(2, body), content_type='application/json')
    body['message'] = '帐号不存在'
    return HttpResponse(encodejson(2, body), content_type='application/json')

@csrf_exempt
def get_pending_orders(req):
    body = {}
    token = req.POST.get('token')
    if not token == 'rapospectreonly':
        body['message'] = '接口访问权限不足'
        return HttpResponse(encodejson(2, body), content_type='application/json')
    order_list = Order.objects.filter(status=1)
    result = []
    if order_list.exists():
        for order in order_list:
            order_info = {}
            order_info['student'] = '学员: {0}|{1}'.format(order.belong.account, order.belong.nick)
            order_info['mentor'] = '教练: {0}|{1}'.format(order.teach_by.account, order.teach_by.nick)
            order_info['info'] = '课程: {0}|价格: {1}|时间: {2}'.format(order.course_name, order.order_price, datetime_to_string(order.create_time))
            result.append(order_info)
        body['new'] = True
    else:
        body['new'] = False
    body['order_list'] = result
    return HttpResponse(encodejson(1, body), content_type='application/json')