from django.conf import settings
from fanfeedr import FanFeedrAPI
from utilities.cache.decorators import cacheable


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
