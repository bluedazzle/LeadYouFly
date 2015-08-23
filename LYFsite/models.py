# -*- coding: utf-8 -*-
from LYFAdmin.models import *
from django import forms


class RegisterForm(forms.Form):
    phone = forms.CharField(max_length=11)
    verify_code = forms.CharField(max_length=6)
    username = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20)


class CompleteInfoForm(forms.Form):
    qq = forms.CharField(max_length=20)
    yy = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=11)


class MentorContactForm(forms.Form):
    qq = forms.CharField(max_length=20)
    yy = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=11)


class UpdateCourseForm(forms.Form):
    id = forms.IntegerField(required=False)
    course_name = forms.CharField(max_length=50)
    course_price = forms.IntegerField()
    course_info = forms.CharField(max_length=500)


class AppraiseOrder(forms.Form):
    order_id = forms.IntegerField()
    stars = forms.IntegerField()
    content = forms.CharField(max_length=100)


class ComplainForm(forms.Form):
    name = forms.CharField(max_length=50)
    qq = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=11)
    mentor_name = forms.CharField(max_length=50)
    complain_content = forms.CharField(max_length=100, required=False)
    check_id = forms.CharField(max_length=10)
    image_list = forms.CharField(max_length=100)


class ChangePasswordForm(forms.Form):
    origin_password = forms.CharField(max_length=20)
    new_password = forms.CharField(max_length=20)
    password_again = forms.CharField(max_length=20)