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
    return render_to_response('common/host.html',
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
        return HttpResponseRedirect('common/teacher_login.html', context_instance=RequestContext(request))


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
        new_user.save()
        phone_verify[0].delete()

        return HttpResponse(json.dumps("success"))


def search_teacher(request):
    return_content = utils.is_login(request)
    if return_content:
        return_content['is_login'] = True
    else:
        return_content = dict()
    heros = Hero.objects.all()
    return_content['heros'] = heros
    if not request.session.get('teach_area'):
        request.session['teach_area'] = ''
    if not request.session.get('teach_position'):
        request.session['teach_position'] = ''
    if not request.session.get('teach_hero'):
        request.session['teach_hero'] = ''

    if request.method == 'GET':
        teach_area = request.GET.get('teach_area')
        teach_position = request.GET.get('teach_position')
        teach_hero = request.GET.get('teach_hero')
        if teach_area:
            request.session['teach_area'] = teach_area

        if teach_position:
            request.session['teach_position'] = teach_position

        if teach_hero:
            request.session['teach_hero'] = teach_hero

        teach_area = request.session.get('teach_area')
        teach_position = request.session.get('teach_position')
        teach_hero = request.session.get('teach_hero')
        if teach_hero and not teach_hero == '0':
            hero_to_teach = Hero.objects.get(id=teach_hero)
        else:
            hero_to_teach = None

        mentors = Mentor.objects.all()
        if teach_area and not teach_area == '0':
            mentors = mentors.filter(teach_area__contains=teach_area)

        if teach_position and not teach_position == '0':
            mentors = mentors.filter(good_at=teach_position)

        if hero_to_teach:
            mentors = mentors.filter(Q(expert_hero1=hero_to_teach) |
                                     Q(expert_hero2=hero_to_teach) |
                                     Q(expert_hero3=hero_to_teach))

        return_content['mentors'] = mentors
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
        return render_to_response('common/search_teacher.html',
                                  return_content)


def about_us(request):
    return render_to_response('common/about_us.html')


def contact_us(request):
    return render_to_response('common/contact_us.html')


def laws(request):
    return render_to_response('common/laws.html')


def problems(request):
    return render_to_response('common/problems.html')


def service(request):
    return render_to_response('common/service.html')


def become_teacher(request):
    return render_to_response('common/become_teacher.html')