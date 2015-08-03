from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
import LYFSite.urls
import LYFAdmin.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LeadYouFly.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^site_admin/', include(admin.site.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIR}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_DIR}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIR}),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FONTS_DIR}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DIR}),
    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.UPLOAD_DIR}),
    url(r'^', include(LYFSite.urls)),
    url(r'^admin/', include(LYFAdmin.urls)),
    url(r'^ueditor/', include('DjangoUeditor.urls' )),
)
