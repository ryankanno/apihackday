from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from fans.views import www_views, fanfeedr_views

urlpatterns = patterns('',

    # www related views
    url(r'^$', www_views.slash, name="slash"),

    # fanfeedr views
    url(r'^leagues/$', fanfeedr_views.leagues, name="leagues"),
    url(r'^leagues/(?P<league>[\-\w\s]+)/games/upcoming$', fanfeedr_views.upcoming_games, name="upcoming_games"),
    url(r'^leagues/(?P<league>[\-\w\s]+)/games/(?P<game>[\w\-]+)$', fanfeedr_views.game_details, name="game_details"),


    # sms related views
    url(r'^sms/update$', www_views.update, name="sms_update"),
)
