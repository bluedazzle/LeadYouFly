from django.conf.urls import patterns, include, url
from LeadYouFly.settings import UPLOAD_DIR
from LYFAdmin import views

urlpatterns = patterns('',
    url(r'^index/$', views.admin_index),
    url(r'^website/$', views.admin_website),
    url(r'^order/$', views.admin_order),
    url(r'^mentor/$', views.admin_mentor),
    url(r'^student/$', views.admin_student),
    url(r'^audit/$', views.admin_audit),
    url(r'^pay/$', views.admin_pay),
    url(r'^pay/stu_rec$', views.admin_pay_stu_rec),
    url(r'^pay/mentor_rec', views.admin_pay_mentor_rec),
    url(r'^pay/cash', views.admin_pay_cash),
    url(r'^mentor/detail/$', views.admin_mentor_detail),
    url(r'^mentor/detail/static/upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': UPLOAD_DIR}),
    url(r'^mentor/info/$', views.admin_mentor_info),
    url(r'^mentor/order/$', views.admin_mentor_order),
    url(r'^student/info/$', views.admin_student_info),
    url(r'^student/order/$', views.admin_student_order),
)
