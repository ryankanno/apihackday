from django.template import RequestContext
from django.shortcuts import render_to_response 

from fans.utils.fanfeedr_helper import get_leagues, get_games, get_event, get_boxscore
from fans.models import Subscription

import operator


def leagues(request):
    sub_dict = {}
    leagues = sorted(get_leagues(), key=operator.itemgetter('name'))
    subs = Subscription.objects.get_league_subs(request.user, [league.get('id') for league in leagues])
    for sub in subs:
        sub_dict[sub.league_id.encode('ascii')] = sub.pk
    return render_to_response('fanfeedr/leagues.html', {'leagues': leagues, 'subs':sub_dict}, 
        context_instance=RequestContext(request))


def upcoming_games(request, league):
    league = filter(lambda x: x['name'] == league, get_leagues())[0]
    upcoming = get_games(id=league['id']) or []
    return render_to_response('fanfeedr/upcoming_games.html', {'games': upcoming, 'league': league}, 
        context_instance=RequestContext(request))


def game_details(request, league, game):
    details = get_event(id=game) or []
    return render_to_response('fanfeedr/game_details.html', {'game_details': details}, 
        context_instance=RequestContext(request))


def game_boxscore(request): 
    boxscore = get_boxscore() or []
    return render_to_response('fanfeedr/game_boxscore.html', {'game_boxscore': boxscore}, 
        context_instance=RequestContext(request))
