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


def host(requset):
    test_array = []
    for i in range(0, 6):
        test_array.append("测试数据!!!这个是测试数据" + str(i))
    return render_to_response('host.html', {"test_array": test_array})


def teacher_host(request):
    return render_to_response('teacher/teacher_host.html')