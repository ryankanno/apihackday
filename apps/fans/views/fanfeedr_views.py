from django.template import RequestContext
from django.shortcuts import render_to_response 

from fans.utils.fanfeedr_helper import get_leagues, get_games, get_event, get_boxscore
from fans.models import Subscription

import operator


def leagues(request):
    leagues = sorted(get_leagues(), key=operator.itemgetter('name'))
    subs = Subscription.objects.get_league_subs(request.user, [league.get('id') for league in leagues])
    for league in leagues:
        try:
            league['sub'] = subs.filter(league_id=str(league.get('id'))).get().pk
        except Exception as e:
            pass

    return render_to_response('fanfeedr/leagues.html', {'leagues': leagues}, 
        context_instance=RequestContext(request))


def upcoming_games(request, league):
    league = filter(lambda x: x['name'] == league, get_leagues())[0]
    upcoming = get_games(id=league['id']) or []

    subs = Subscription.objects.get_game_subs(request.user, [u.get('id') for u in upcoming])
    for game in upcoming:
        try:
            game['sub'] = subs.filter(game_id=str(game.get('id'))).get().pk
        except Exception as e:
            print e
            pass

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
