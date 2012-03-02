from fans.utils.fanfeedr_helper import *
from fan.subscriptions import *

def is_subsciption_game(sub):
    return True if sub.game_id else False

def is_subsciption_team(sub):
    return True if sub.team_id else False

def is_subsciption_league(sub):
    return True if sub.league_id else False

def subcription_handler(sub):
    # get all of today's games for given subscription type whether league, team or game
    games = []
    if is_subscription_game():
        games = [ get_event(id=sub.event_id) ]
    elif is_subscription_team():
        games = get_games("teams", id=sub.team_id, today=True)
        games = [ get_event(id=game['id']) for game in games ]
    elif: # must be a league subscription
        games = get_games("leagues", id=sub.league_id, today=True)
        games = [ get_event(id=game['id']) for game in games ]

    for game in games:
        if sub_rules.alert_on_game(game):
            return True

