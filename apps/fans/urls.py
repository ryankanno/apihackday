from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from fans.views import www_views, fanfeedr_views, subscription_views

urlpatterns = patterns('',

    # www related views
    url(r'^$', www_views.slash, name="slash"),

    url(r'^test/$', fanfeedr_views.game_boxscore, name="test"),

    # fanfeedr views
    url(r'^leagues/$', fanfeedr_views.leagues, name="leagues"),
    url(r'^leagues/(?P<league>[\-\w\s]+)/games/upcoming$', fanfeedr_views.upcoming_games, name="upcoming_games"),
    url(r'^leagues/(?P<league>[\-\w\s]+)/games/(?P<game>[\w\-]+)$', fanfeedr_views.game_details, name="game_details"),
    
    # subscription views
    url(r'^subscriptions/$', subscription_views.details, name="subscription_details"),
    url(r'^subscriptions/subscribe$', subscription_views.subscribe, name="subscription_subscribe"),
    url(r'^subscriptions/unsubscribe$', subscription_views.unsubscribe, name="subscription_unsubscribe"),
)
