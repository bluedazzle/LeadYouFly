# -*- coding: utf-8 -*-
from LYFAdmin.models import *
import LYFAdmin.sms
import random
from django.http import HttpResponse
import json
import datetime


def send_verify_code(phone):
    verify_code = str(random.randint(100000, 999999))
    sms_res = LYFAdmin.sms.send_msg(str(phone), verify_code)
    if sms_res:
        try:
            phone_has = PhoneVerify.objects.get(phone=phone)
            phone_has.verify = verify_code
            phone_has.save()
        except PhoneVerify.DoesNotExist:
            new_phone_verify = PhoneVerify()
            new_phone_verify.phone = phone
            new_phone_verify.verify = verify_code
            new_phone_verify.save()

        return True
    else:
        return False


def get_floor(number):
    return float(unicode('%0.2f' % number)[:-1])


def get_verify_code(request):
    if request.method == 'GET':
        phone = request.GET.get('phone')
        if len(phone) == 11:
            phone_has_register = Student.objects.filter(account=phone)
            if phone_has_register.count() > 0:
                return HttpResponse(json.dumps(u"该手机号已注册"))
            phone_has = PhoneVerify.objects.filter(phone=phone)
            if phone_has.count() > 0:
                if phone_has[0].is_get_again():
                    pass
                else:
                    return HttpResponse(json.dumps(u"不要短时间内多次获取验证码"))

            if send_verify_code(phone):
                return HttpResponse(json.dumps("success"))
            else:
                return HttpResponse(json.dumps(u"发送验证码失败"))

        else:
            return HttpResponse(json.dumps(u"错误的电话号码"))


def get_verify_code_forget(request):
    if request.method == 'GET':
        phone = request.GET.get('phone')
        if len(phone) == 11:
            stu_has_register = Student.objects.filter(account=phone)
            mentor_has_register = Mentor.objects.filter(account=phone)
            if stu_has_register.count() == 0 and mentor_has_register.count() == 0:
                return HttpResponse(json.dumps(u"该用户不存在"))
            phone_has = PhoneVerify.objects.filter(phone=phone)
            if phone_has.count() > 0:
                if phone_has[0].is_get_again():
                    pass
                else:
                    return HttpResponse(json.dumps(u"不要短时间内多次获取验证码"))

            if send_verify_code(phone):
                return HttpResponse(json.dumps("success"))
            else:
                return HttpResponse(json.dumps(u"发送验证码失败"))

        else:
            return HttpResponse(json.dumps(u"错误的电话号码"))


def is_login(request):
    content = dict()
    student_account = request.session.get('student')
    teacher_account = request.session.get('teacher')
    if student_account:
        content['login_type'] = "student"
        content['active_user'] = Student.objects.get(account=request.session.get('student'))
        content['is_login'] = True
        return content
    elif teacher_account:
        content['login_type'] = "teacher"
        content['mentor'] = Mentor.objects.get(account=request.session.get('teacher'))
        finish_course = Order.objects.filter(teach_by=content['mentor'],
                                             status=3)
        appraise_course = Order.objects.filter(teach_by=content['mentor'],
                                               status=4)
        content['teach_courses'] = finish_course.count() + appraise_course.count()
        teach_student = list()
        for course in finish_course:
            if course.belong not in teach_student:
                teach_student.append(course.belong)
        for course in appraise_course:
            if course.belong not in teach_student:
                teach_student.append(course.belong)
        content['teach_students'] = len(teach_student)
        content['is_login'] = True
        return content
    else:
        return False


def get_all_heroes(request):
    if request.method == 'GET':
        heroes = Hero.objects.all()
        hero_list = []
        for hero in heroes:
            hero_list.append({
                'id': hero.id,
                'hero_name': hero.hero_name,
                'hero_pic': hero.hero_picture
            })

        return HttpResponse(json.dumps(hero_list))


def check_status(mentor):
    order_list = mentor.men_orders.filter(status=2).order_by('-teach_end_time')
    if order_list.count() > 0:
        order = order_list[0]
        end_time = order.teach_end_time
        now_time = datetime.datetime.now(tz=get_current_timezone())
        if now_time > end_time:
            return True
        else:
            return False
    return True