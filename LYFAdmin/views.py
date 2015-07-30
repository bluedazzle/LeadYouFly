from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

# Create your views here.

def admin_index(req):
    return render_to_response('index_admin.html')


def admin_order(req):
    return render_to_response('order_admin.html')


def admin_mentor(req):
    return render_to_response('mentor_admin.html')


def admin_student(req):
    return render_to_response('student_admin.html')


def admin_audit(req):
    return render_to_response('audit_admin.html')


def admin_pay(req):
    return render_to_response('pay_admin.html')


def admin_mentor_detail(req):
    return render_to_response('mentor_detail_admin.html')


def admin_student_detail(req):
    return render_to_response('student_detail_admin.html')