from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
                       url('^host$', host),
                       url('^teacher_host$', teacher_host),
                       )