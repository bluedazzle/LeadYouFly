from django.conf.urls import patterns, include, url
from LYFAdmin import views

urlpatterns = patterns('',
    url(r'^index/$', views.admin_index),
    url(r'^order/$', views.admin_order),
    url(r'^mentor/$', views.admin_mentor),
    url(r'^student/$', views.admin_student),
    url(r'^audit/$', views.admin_audit),
    url(r'^pay/$', views.admin_pay),
    url(r'^mentor_detail/$', views.admin_mentor_detail),
    url(r'^student_detail/$', views.admin_student_detail),
)
