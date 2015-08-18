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