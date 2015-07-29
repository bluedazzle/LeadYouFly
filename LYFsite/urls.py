from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
                       url('^host$', host),

                       # teacher

                       url('^teacher/host$', teacher_host),
                       url('^teacher/contact$', teacher_contact),
                       url('^teacher/indemnity$', teacher_indemnity),
                       url('^teacher/order_accept$', order_accept),
                       url('^teacher/manage_courses$', manage_courses),
                       url('^teacher/upload_video$', teacher_video_upload),

                       # user

                       url('^user/message$', user_message),

                       url('^$', test)
                       )