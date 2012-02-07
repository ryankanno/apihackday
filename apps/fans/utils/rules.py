from fans.utils.fanfeedr_helper import *

def game_almost_over(game):
    scores = get_boxscore()
    return False

# should we notify for this league
def should_notify_league(league):
    # TODO : if league has any exciting games
    return False

# should we notify for this league
def should_notify_team(team):
    # TODO : if team has any exciting games
    scores = get_boxscore()

    #start_time = if scores['scoring_detail'][time left]
    #current_time = ...
    # run_time = ...
    
    if team == "NY Giants":
        return True

if __name__ == "__main__":
    print get_boxscore().keys()
