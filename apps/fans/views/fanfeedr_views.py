from django.template import RequestContext
from django.shortcuts import render_to_response 

from fans.utils.fanfeedr_helper import get_leagues, get_event, get_boxscore, get_recap, get_lineup
from fans.utils.fanfeedr_helper import get_previous_games
from fans.utils.fanfeedr_helper import get_todays_games
from fans.utils.fanfeedr_helper import get_upcoming_games
from fans.models import Subscription

import operator
import iso8601
import datetime
from operator import itemgetter


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


def _get_games(user, league, fun, server_ts):
    games  = fun(id=league['id']) or []
    subs   = Subscription.objects.get_game_subs(user, [g.get('id') for g in games])

    for game in games:
        try:
            game['sub'] = subs.filter(game_id=str(game.get('id'))).get().pk
        except Exception as e:
            pass

        try:
            game['datetime'] = iso8601.parse_date(game['date'])
        except Exception as e:
            game['datetime'] = datetime.datetime.min

        game['has_started'] = (server_ts > game['datetime'].replace(tzinfo=None))

    
    return sorted(games, key=itemgetter('date'), reverse=True)


def previous_games(request, league):
    server_ts = datetime.datetime.utcnow()
    league = filter(lambda x: x['name'] == league, get_leagues())[0]
    games     = _get_games(request.user, league, get_previous_games, server_ts)

    return render_to_response('fanfeedr/previous_games.html', 
        {'games': games, 'server_ts': server_ts,
         'league': league}, context_instance=RequestContext(request))


def todays_games(request, league):
    server_ts = datetime.datetime.utcnow()
    league    = filter(lambda x: x['name'] == league, get_leagues())[0]
    games     = _get_games(request.user, league, get_todays_games, server_ts)

    return render_to_response('fanfeedr/todays_games.html', 
        {'games': games, 'server_ts': server_ts,
         'league': league}, context_instance=RequestContext(request))


def upcoming_games(request, league):
    server_ts = datetime.datetime.utcnow()
    league    = filter(lambda x: x['name'] == league, get_leagues())[0]
    games     = _get_games(request.user, league, get_upcoming_games, server_ts)

    return render_to_response('fanfeedr/upcoming_games.html', 
        {'games': games, 'server_ts': server_ts,
         'league': league}, context_instance=RequestContext(request))


def game_details(request, league, game):
    details = get_event(id=game) or []
    boxscore = get_boxscore(id=game) or []
    #recap    = get_recap(id=game) or []
    recap = []
    lineup   = get_lineup(id=game) or []
    return render_to_response('fanfeedr/game_details.html', 
        {'game_details': details, 'game_boxscore': boxscore, 'game_recap': recap, 'game_lineup': lineup},
        context_instance=RequestContext(request))
