from django.conf.urls import patterns, include, url
from views import *
import user_view
import teacher_view

urlpatterns = patterns('',
                       url('^$', host),

                       # common

                       url('^login$', login),
                       url('^register$', register),

                       # teacher

                       url('^teacher/host$', teacher_view.teacher_host),
                       url('^teacher/contact$', teacher_view.teacher_contact),
                       url('^teacher/indemnity$', teacher_view.teacher_indemnity),
                       url('^teacher/order_accept$', teacher_view.order_accept),
                       url('^teacher/manage_courses$', teacher_view.manage_courses),
                       url('^teacher/upload_video$', teacher_view.teacher_video_upload),

                       # user

                       url('^user/message$', user_view.user_message),
                       url('^user/complete_mes$', user_view.complete_mes),
                       url('^user/my_order$', user_view.my_order),
                       url('^test$', test)
                       )