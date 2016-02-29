from django.conf.urls import patterns, include, url
from LYFApi import views

urlpatterns = patterns('',
                       url(r'^login$', views.login),)