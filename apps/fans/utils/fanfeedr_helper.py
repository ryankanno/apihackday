from django.conf import settings
from fanfeedr import FanFeedrAPI
from utilities.cache.decorators import cacheable

import datetime
import logging

LOG = logging.getLogger(__name__)

FANFEEDR_API_KEY = getattr(settings, 'FANFEEDR_API_KEY', None)
FANFEED_TIER     = getattr(settings, 'FANFEEDR_TIER', None)
VERSION          = "1"

YEAR_CACHE = 60*60*24*365


@cacheable(ttl=YEAR_CACHE)
def get_leagues(version=VERSION):
    LOG.info("Calling get_leagues")
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    try:
        leagues = api.get_collection("leagues")
    except Exception as e:
        LOG.error("Exception occurred calling get_leagues", e)
        leagues = []
    return leagues


@cacheable(ttl=60*60*4)
def get_upcoming_games(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    return api.get_collection_method("next", "events", ptype="leagues", puid=id)


@cacheable(ttl=YEAR_CACHE)
def get_previous_games(version=VERSION, id=None):
    LOG.info("Calling get_previous_games")
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    try:
        games = api.get_collection_method("last", "events", ptype="leagues", puid=id)
    except Exception as e:
        LOG.error("Exception calling get_previous_games", e)
        games = []
    return games


@cacheable(ttl=60*60*1)
def get_todays_games(version=VERSION, id=None):
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    return api.get_collection_method("today", "events", ptype="leagues", puid=id)


@cacheable(ttl=60*60*4)
def get_event(version=VERSION, id=None):
    LOG.info("Calling get_event")
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    try:
        evt = api.get_resource("events", id)
    except Exception as e:
        LOG.error("Exception occurred calling get_event", e)
        evt = {}
    return evt


@cacheable(ttl=YEAR_CACHE)
def get_boxscore(version=VERSION, id=None):
    LOG.info("Calling get_boxscore")
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    try:
        bs = api.get_collection("boxscore", "events", id)
    except Exception as e:
        LOG.error("Exception occurred calling get_boxscore", e)
        bs = {}
    return bs


def get_lineup(version=VERSION, id=None):
    LOG.info("Calling get_lineup")
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    return api.get_collection("lineup", "events", id)


def get_recap(version=VERSION, id=None):
    LOG.info("Calling get_recap for game(id={0})".format(id))
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=FANFEEDR_TIER) 
    try:
        recap = api.get_collection("recap", "events", id)
    except Exception as e:
        LOG.error("Exception occurred calling get_recap", e)
        recap = []
    return recap 


import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)


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
