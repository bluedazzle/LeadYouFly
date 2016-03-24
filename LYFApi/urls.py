from django.conf.urls import patterns, include, url
from LYFApi import views

urlpatterns = patterns('',
                       url(r'^login$', views.login),
                       url(r'^pending_orders$', views.get_pending_orders),
                       url(r'^test$', views.test),
                       )