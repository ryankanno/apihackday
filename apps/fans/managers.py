from django.db import models
from itertools import chain


class SubscriptionManager(models.Manager):

    def notify(self, league_id=None, team_id=None, game_id=None):

        league_subs = self.filter(league_id=league_id) if league_id else self.none()
        team_subs   = self.filter(team_id=team_id) if team_id else self.none()
        game_subs   = self.filter(game_id=game_id) if game_id else self.none()

        return list(chain(league_subs, team_subs, game_subs))
