from django.conf import settings
from fanfeedr import FanFeedrAPI
from utilities.cache.decorators import cacheable

import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)


FANFEEDR_API_KEY = getattr(settings, 'FANFEEDR_API_KEY', None)
TIER = getattr(settings, 'TIER', None)
VERSION = "1"


@cacheable(ttl=60*60*4)
def get_leagues(version=VERSION):
    print "Calling Leagues"
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection("leagues")


@cacheable(ttl=60*60*4)
def get_games(version=VERSION, id=None):
    print "Calling Games"
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection_method("next", "events", ptype="leagues", puid=id)


@cacheable(ttl=60*60*4)
def get_event(version=VERSION, id=None):
    print "Get Event"
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_resource("events", id)


def get_boxscore(version=VERSION, id=None):
    id = '5b1be5b0-a636-5e1a-bde6-e643f4584db2'
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier=TIER) 
    return api.get_collection("boxscore", "events", id)


def add_game(date, game_id):
    games = r.get('games-%s' % date)

    if game_id not in games:
        games.append(game_id)

    r.set('games-%s' % date, games)


def get_game(date):
    return r.get('games-%s' % date)


def cache_all_games():
    leagues = get_leagues()
    for league in leagues:
        games = get_games(league.id)
        for game in games:
            game['league'] = league

            dtstr = game['date']
            dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.000000Z")
            add_game(dt.strftime("%Y-%m-%d"), game['id'])
