from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
                       url('^host$', host),
                       url('^teacher/host$', teacher_host),
                       url('^teacher/contact$', teacher_contact),
                       url('^teacher/indemnity$', teacher_indemnity),
                       url('^teacher/order_accept$', order_accept),
                       )