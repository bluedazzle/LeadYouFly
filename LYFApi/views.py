# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from LYFAdmin.models import Student
# Create your views here.

import json

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