from django.conf.urls import patterns, include, url
from LeadYouFly.settings import UPLOAD_DIR
from LYFAdmin import views

urlpatterns = patterns('',
                       # url(r'^index/$', views.admin_index),
                       # url(r'^get_status/$', views.admin_get_status),
                       url(r'^$', views.admin_login_page),
                       url(r'^login/$', views.admin_login),
                       url(r'^logout/$', views.admin_log_out),
                       # url(r'^index/change_video$', views.admin_index_change_video),
                       # url(r'^index/new_video', views.admin_index_new_video),
                       # url(r'^index/change_recommend$', views.admin_index_change_recommend),
                       # url(r'^index/change_picture', views.admin_index_change_picture),
                       url(r'^portal/$', views.admin_portal),
                       url(r'^complain/$', views.admin_complain),
                       # url(r'^complain/image/(?P<rid>(\d)+)/$', views.admin_complain_picture),
                       # url(r'^complain/finish/(?P<rid>(\d)+)/$', views.admin_complain_finish),
                       url(r'^portal/change_password/$', views.admin_portal_change_password),
                       # url(r'^website/$', views.admin_website),
                       # url(r'^website/del_hero$', views.admin_website_del_hero),
                       # url(r'^website/new_hero$', views.admin_website_new_hero),
                       # url(r'^website/modify_hero$', views.admin_website_modify_hero),
                       # url(r'^website/new_notice$', views.admin_website_new_notice),
                       # url(r'^website/del_notice/(?P<nid>(\d)+)/$', views.admin_website_del_notice),
                       # url(r'^website/modify_notice/(?P<nid>(\d)+)/$', views.admin_website_modify_page),
                       # url(r'^website/notice/modify/(?P<nid>(\d)+)/$', views.admin_website_modify),
                       # url(r'^website/notice/(?P<nid>(\d)+)/$', views.admin_website_notice_detail),
                       # url(r'^message/$', views.admin_message),
                       # url(r'^message/new_message$', views.admin_message_new),
                       # url(r'^order/$', views.admin_order),
                       # url(r'^order/search$', views.admin_order_search),
                       # url(r'^order/output', views.admin_order_output),
                       # url(r'^mentor/$', views.admin_mentor),
                       # url(r'^patner/$', views.admin_patner),
                       # url(r'^mentor/new_mentor$', views.admin_mentor_new_mentor),
                       # url(r'^student/$', views.admin_student),
                       # url(r'^student/search/$', views.admin_student_search),
                       # url(r'^audit/pass/(?P<oid>(\d)+)/$', views.admin_audit_pass),
                       # url(r'^audit/reject/(?P<oid>(\d)+)/$', views.admin_audit_reject),
                       # url(r'^audit/$', views.admin_audit),
                       # url(r'^pay/$', views.admin_pay),
                       # url(r'^pay/freeze/(?P<mid>(\d)+)/$', views.admin_pay_freeze),
                       # url(r'^pay/thaw/(?P<mid>(\d)+)/$', views.admin_pay_thaw),
                       # url(r'^pay/commission/(?P<mid>(\d)+)/$', views.admin_get_commission),
                       # url(r'^pay/stu_rec$', views.admin_pay_stu_rec),
                       # url(r'^pay/mentor_rec', views.admin_pay_mentor_rec),
                       # url(r'^pay/cash/confirm/(?P<cid>(\d)+)/', views.admin_pay_agree_cash),
                       # url(r'^pay/cash/rejected/(?P<cid>(\d)+)/', views.admin_pay_rejected_cash),
                       # url(r'^pay/cash', views.admin_pay_cash),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/$', views.admin_mentor_detail),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/change_video$', views.admin_mentor_change_video),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/new_course', views.admin_mentor_new_course),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/del_course/(?P<cid>(\d)+)/', views.admin_mentor_del_course),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/new_video', views.admin_mentor_new_video),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/new_picture', views.admin_mentor_new_picture),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/update_detail/$', views.admin_mentor_update_detail),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/del_hero/(?P<hid>(\d)+)/$', views.admin_mentor_del_hero),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/add_hero/$', views.admin_mentor_add_hero),
                       # url(r'^mentor/detail/(?P<mid>(\d)+)/change_price/(?P<cid>(\d)+)/$',
                       #     views.admin_mentor_change_price),
                       # url(r'^mentor/detail/(\d)+/static/upload/(?P<path>.*)$', 'django.views.static.serve',
                       #     {'document_root': UPLOAD_DIR}),
                       # url(r'^mentor/info/(?P<mid>(\d)+)/$', views.admin_mentor_info),
                       # url(r'^mentor/info/(?P<mid>(\d)+)/change_priority/$', views.admin_mentor_change_priority),
                       # url(r'^mentor/order/(?P<mid>(\d)+)/$', views.admin_mentor_order),
                       # url(r'^student/info/(?P<sid>(\d)+)/$', views.admin_student_info),
                       # url(r'^student/info/(?P<sid>(\d)+)/modify_exp/$', views.admin_student_modify_exp),
                       # url(r'^student/order/(?P<sid>(\d)+)/$', views.admin_student_order),
                       url(r'^wechat/$', views.admin_wechat),
                       url(r'^wechat/jzws$', views.admin_wechat_jzws),
                       url(r'^wechat/setting$', views.admin_wechat_setting),
                       url(r'^wechat/refresh$', views.admin_wechat_refresh),
                       url(r'^wechat/new_channel', views.admin_wechat_new_channel),
                       url(r'^wechat/channel/detail/(?P<pid>(\d)+)/$', views.admin_wechat_detail),
                       url(r'^wechat/channel/output/(?P<pid>(\d)+)/$', views.admin_wechat_output),
                       url(r'^wechat/kefu$', views.admin_wechat_kefu),
                       url(r'^wechat/kefu/distribution$', views.admin_wechat_kefu_distribution),
                       url(r'^promotion$', views.promotion),
                       url(r'^promotion/login$', views.promotion_login),

)
