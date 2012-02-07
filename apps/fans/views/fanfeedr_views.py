from django.template import RequestContext
from django.shortcuts import render_to_response 

from fans.utils.fanfeedr_helper import get_leagues, get_event, get_boxscore, get_recap, get_lineup
from fans.utils.fanfeedr_helper import get_previous_games
from fans.utils.fanfeedr_helper import get_todays_games
from fans.utils.fanfeedr_helper import get_upcoming_games
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


def previous_games(request, league):
    league = filter(lambda x: x['name'] == league, get_leagues())[0]
    previous = get_previous_games(id=league['id']) or []

    subs = Subscription.objects.get_game_subs(request.user, [g.get('id') for g in previous])
    for game in previous:
        try:
            game['sub'] = subs.filter(game_id=str(game.get('id'))).get().pk
        except Exception as e:
            pass

    return render_to_response('fanfeedr/previous_games.html', 
        {'games': previous, 'league': league}, context_instance=RequestContext(request))


def todays_games(request, league):
    league = filter(lambda x: x['name'] == league, get_leagues())[0]
    today = get_todays_games(id=league['id']) or []

    subs = Subscription.objects.get_game_subs(request.user, [g.get('id') for g in today])
    for game in today:
        try:
            game['sub'] = subs.filter(game_id=str(game.get('id'))).get().pk
        except Exception as e:
            pass

    return render_to_response('fanfeedr/todays_games.html', 
        {'games': today, 'league': league}, context_instance=RequestContext(request))


def upcoming_games(request, league):
    league = filter(lambda x: x['name'] == league, get_leagues())[0]
    upcoming = get_upcoming_games(id=league['id']) or []

    subs = Subscription.objects.get_game_subs(request.user, [g.get('id') for g in upcoming])
    for game in upcoming:
        try:
            game['sub'] = subs.filter(game_id=str(game.get('id'))).get().pk
        except Exception as e:
            pass

    return render_to_response('fanfeedr/upcoming_games.html', 
        {'games': upcoming, 'league': league}, context_instance=RequestContext(request))


def game_details(request, league, game):
    details = get_event(id=game) or []
    boxscore = get_boxscore(id=game) or []
    #recap    = get_recap(id=game) or []
    recap = []
    lineup   = get_lineup(id=game) or []
    return render_to_response('fanfeedr/game_details.html', 
        {'game_details': details, 'game_boxscore': boxscore, 'game_recap': recap, 'game_lineup': lineup},
        context_instance=RequestContext(request))
