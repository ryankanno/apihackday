from django.conf import settings
from fanfeedr import FanFeedrAPI
from utilities.cache.decorators import cacheable

import datetime

import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

FANFEEDR_API_KEY = getattr(settings, 'FANFEEDR_API_KEY', None)
TIER = getattr(settings, 'TIER', None)
VERSION = "1"


@cacheable(ttl=60*60*4)
def get_leagues(version=VERSION):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection("leagues")


@cacheable(ttl=60*60*4)
def get_upcoming_games(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection_method("next", "events", ptype="leagues", puid=id)


@cacheable(ttl=60*60*4)
def get_previous_games(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection_method("last", "events", ptype="leagues", puid=id)


@cacheable(ttl=60*60*1)
def get_todays_games(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection_method("today", "events", ptype="leagues", puid=id)


@cacheable(ttl=60*60*4)
def get_event(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_resource("events", id)


def get_boxscore(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection("boxscore", "events", id)


def get_lineup(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection("lineup", "events", id)


def get_recap(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection("recap", "events", id)


def add_game(date, game_id):
    games = r.get('games-%s' % date)

    if games is not None:
        if game_id not in games:
            games.append(game_id)

        r.set('games-%s' % date, games)


def get_game(date):
    return r.get('games-%s' % date)


def cache_all_games():
    leagues = get_leagues()
    for league in leagues:
        try:
            games = get_games(id=league['id'])
            for game in games:
                game['league'] = league

                dtstr = game['date']
                dt = datetime.datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%S.000000Z")
                add_game(dt.strftime("%Y-%m-%d"), game['id'])
        except Exception as e:
            pass
