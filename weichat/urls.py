from django.conf.urls import patterns, include, url
from LeadYouFly.settings import UPLOAD_DIR
from weichat.views import *

urlpatterns = patterns('',
                       url(r'^$', wechat_service),

)
