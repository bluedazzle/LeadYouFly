# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

from forms import MentorDetailContentForm

# Create your views here.

def admin_index(req):
    return render_to_response('index_admin.html')


def admin_website(req):
    return render_to_response('website_admin.html')


def admin_order(req):
    return render_to_response('order_admin.html')


def admin_mentor(req):
    return render_to_response('mentor_admin.html')


def admin_student(req):
    return render_to_response('student_admin.html')


def admin_audit(req):
    return render_to_response('audit_admin.html')


def admin_pay(req):
    return render_to_response('pay_mentor_admin.html')


def admin_pay_stu_rec(req):
    return render_to_response('pay_stu_rec.html')


def admin_pay_mentor_rec(req):
    return render_to_response('pay_mentor_rec.html')


def admin_pay_cash(req):
    return render_to_response('pay_cash.html')


def admin_mentor_detail(req):
    form = MentorDetailContentForm(initial={'Mentor_Detail': '测试'})
    return render_to_response('mentor_detail_admin.html', {'form': form})


def admin_mentor_info(req):
    return render_to_response('mentor_info_admin.html')


def admin_mentor_order(req):
    return render_to_response('mentor_order_admin.html')


def admin_student_info(req):
    return render_to_response('student_info_admin.html')


def admin_student_order(req):
    return render_to_response('student_order_admin.html')