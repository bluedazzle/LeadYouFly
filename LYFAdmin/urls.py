from django.conf.urls import patterns, include, url
from LeadYouFly.settings import UPLOAD_DIR
from LYFAdmin import views

urlpatterns = patterns('',
    url(r'^index/$', views.admin_index),
    url(r'^index/change_recommend$', views.admin_index_change_recommend),
    url(r'^index/change_picture', views.admin_index_change_picture),
    url(r'^website/$', views.admin_website),
    url(r'^website/del_hero$', views.admin_website_del_hero),
    url(r'^website/new_hero$', views.admin_website_new_hero),
    url(r'^order/$', views.admin_order),
    url(r'^order/search$', views.admin_order_search),
    url(r'^mentor/$', views.admin_mentor),
    url(r'^mentor/new_mentor$', views.admin_mentor_new_mentor),
    url(r'^student/$', views.admin_student),
    url(r'^audit/$', views.admin_audit),
    url(r'^pay/$', views.admin_pay),
    url(r'^pay/freeze/(?P<mid>(\d)+)/$', views.admin_pay_freeze),
    url(r'^pay/thaw/(?P<mid>(\d)+)/$', views.admin_pay_thaw),
    url(r'^pay/stu_rec$', views.admin_pay_stu_rec),
    url(r'^pay/mentor_rec', views.admin_pay_mentor_rec),
    url(r'^pay/cash/confirm/(?P<cid>(\d)+)/', views.admin_pay_agree_cash),
    url(r'^pay/cash/rejected/(?P<cid>(\d)+)/', views.admin_pay_rejected_cash),
    url(r'^pay/cash', views.admin_pay_cash),
    url(r'^mentor/detail/(?P<mid>(\d)+)/$', views.admin_mentor_detail),
    url(r'^mentor/detail/(?P<mid>(\d)+)/update_detail/$', views.admin_mentor_update_detail),
    url(r'^mentor/detail/(?P<mid>(\d)+)/del_hero/(?P<hid>(\d)+)/$', views.admin_mentor_del_hero),
    url(r'^mentor/detail/(?P<mid>(\d)+)/add_hero/$', views.admin_mentor_add_hero),
    url(r'^mentor/detail/(?P<mid>(\d)+)/change_price/(?P<cid>(\d)+)/$', views.admin_mentor_change_price),
    url(r'^mentor/detail/(\d)+/static/upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': UPLOAD_DIR}),
    url(r'^mentor/info/(?P<mid>(\d)+)/$', views.admin_mentor_info),
    url(r'^mentor/order/(?P<mid>(\d)+)/$', views.admin_mentor_order),
    url(r'^student/info/(?P<sid>(\d)+)/$', views.admin_student_info),
    url(r'^student/order/(?P<sid>(\d)+)/$', views.admin_student_order),
)
