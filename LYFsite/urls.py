from django.conf.urls import patterns, include, url
from views import *
import user_view
import teacher_view
import utils

urlpatterns = patterns('',
                       url('^$', host),

                       # common

                       url('^login$', login),
                       url('^register$', register),
                       url('^get_verify_sms$', utils.get_verify_code),
                       url('^search_teacher$', search_teacher),
                       url('^mentor_detail$', teacher_detail),
                       url('^about_us$', about_us),
                       url('^contact_us$', contact_us),
                       url('^become_mentor$', become_teacher),
                       url('^laws$', laws),
                       url('^problems$', problems),
                       url('^service$', service),
                       url('^logout$', logout),

                       # teacher

                       url('^teacher/login$', teacher_view.teacher_login),
                       url('^teacher/host$', teacher_view.teacher_host),
                       url('^teacher/contact$', teacher_view.teacher_contact),
                       url('^teacher/indemnity$', teacher_view.teacher_indemnity),
                       url('^teacher/order_accept$', teacher_view.order_accept),
                       url('^teacher/manage_courses$', teacher_view.manage_courses),
                       url('^teacher/upload_video$', teacher_view.teacher_video_upload),

                       # user

                       url('^user/message$', user_view.user_message),
                       url('^user/complete_mes$', user_view.complete_mes),
                       url('^user/my_orders$', user_view.my_orders),
                       url('^user/confirm_order$', user_view.confirm_order),
                       url('^user/follow_mentor$', user_view.follow_mentor),
                       url('^user/cancel_follow$', user_view.cancel_follow),
                       url('^user/my_follow_mentors$', user_view.my_follow_mentors),
                       url('^user/appraise_order$', user_view.appraise_order),
                       url('^test$', test),
                       )