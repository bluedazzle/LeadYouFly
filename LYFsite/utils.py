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


def get_verify_code(request):
    if request.method == 'GET':
        phone = request.GET.get('phone')
        if len(phone) == 11:
            phone_has_register = Student.objects.filter(phone=phone)
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


def is_login(request, account_type):
    if account_type == "student":
        student_account = request.session.get('student')
        if student_account:
            return Student.objects.get(account=request.session.get('student'))
        else:
            return False
    else:
        teacher_account = request.session.get('teacher')
        if teacher_account:
            return Mentor.objects.get(account=request.session.get('teacher'))