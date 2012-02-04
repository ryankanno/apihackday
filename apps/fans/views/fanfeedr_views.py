from django.template import RequestContext
from django.shortcuts import render_to_response 

from fans.utils.fanfeedr_helper import get_leagues, get_games, get_event, get_boxscore

import operator


def leagues(request):
    leagues = sorted(get_leagues(), key=operator.itemgetter('name'))
    return render_to_response('fanfeedr/leagues.html', {'leagues': leagues}, 
        context_instance=RequestContext(request))


def upcoming_games(request, league):
    id = filter(lambda x: x['name'] == league, get_leagues())[0]
    upcoming = get_games(id=id['id']) or []
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
