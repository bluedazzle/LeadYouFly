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


def test(request):
    test_list = range(0, 5)
    return render_to_response('test.html', {'test_list': test_list})


def host(requset):
    test_array = []
    for i in range(0, 6):
        test_array.append("测试数据!!!这个是测试数据" + str(i))
    return render_to_response('host.html', {"test_array": test_array})


def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', context_instance=RequestContext(request))


def register(request):
    if request.method == 'GET':
        return render_to_response('register.html', context_instance=RequestContext(request))