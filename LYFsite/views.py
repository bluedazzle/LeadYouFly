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
from models import *
import json
import utils


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
        test_array = []
        for i in range(0, 6):
            test_array.append("测试数据!!!这个是测试数据" + str(i))
        return_content['test_array'] = test_array
        return_content['test_list'] = range(0, 4)
    return render_to_response('host.html',
                              return_content)


def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))
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


def register(request):
    if request.method == 'GET':
        return render_to_response('register.html', context_instance=RequestContext(request))
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
        new_user.save()
        phone_verify[0].delete()

        return HttpResponse(json.dumps("success"))


def search_teacher(request):
    return_content = utils.is_login(request)
    if return_content:
        return_content['is_login'] = True
    else:
        return_content = dict()

    return_content['test_list'] = range(0, 10)
    if request.method == 'GET':
        return render_to_response('search_teacher.html',
                                  return_content)