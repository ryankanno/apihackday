from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from fans.views import www_views

urlpatterns = patterns('',

    # www related views
    url(r'^$', www_views.slash, name="slash"),

    # sms related views
    url(r'^sms/update$', www_views.update, name="sms_update"),
)
