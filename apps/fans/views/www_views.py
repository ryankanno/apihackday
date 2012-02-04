from django.template import RequestContext
from django.shortcuts import render_to_response 
from django.conf import settings

from fanfeedr import FanFeedrAPI
from utilities.cache.decorators import cacheable


FANFEEDR_API_KEY = getattr(settings, 'FANFEEDR_API_KEY', None)

#"http://ffapi.fanfeedr.com/basic/api/leagues/f65226d8-fbf7-5033-a7a0-50de55b57968/events?api_key=mykey

def slash(request):
    leagues = get_leagues()
    return render_to_response('www/slash.html', {'leagues': leagues}, 
        context_instance=RequestContext(request))


def update(request):
    return render_to_response('www/slash.html', {}, 
        context_instance=RequestContext(request))


@cacheable(ttl=60)
def get_leagues():
    api = FanFeedrAPI(FANFEEDR_API_KEY, tier="basic") 
    return api.get_collection("leagues")
