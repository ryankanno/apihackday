from django.db import models
from itertools import chain


class SubscriptionManager(models.Manager):

    def notify(self, league_id=None, team_id=None, game_id=None):

        league_subs = self.filter(league_id=league_id) if league_id else self.none()
        team_subs   = self.filter(team_id=team_id) if team_id else self.none()
        game_subs   = self.filter(game_id=game_id) if game_id else self.none()

        return list(chain(league_subs, team_subs, game_subs))

    def get_league_subs(self, user, league_ids=None):
        if league_ids is None:
            return self.filter(league_id__isnull=False, team_id__isnull=True,
                    game_id__isnull=True, created_by=user.pk)
        else:
            return self.filter(league_id__in=league_ids, team_id__isnull=True, 
                    game_id__isnull=True, created_by=user.pk)

    def get_team_subs(self, user, league_id=None, team_id=None):
        if league_id is None and team_id is None:
            return self.filter(league_id__isnull=False, team_id__isnull=False, 
                    game_id__isnull=True, created_by=user.id)
        else:
            return self.filter(league_id=league_id, team_id=team_id, 
                    game_id__isnull=True, created_by=user.id)

    def get_game_subs(self, user, game_ids=None):
        if game_ids is None:
            return self.filter(game_id__isnull=False, created_by=user.id)
        else:
            return self.filter(game_id__in=game_ids, created_by=user.id)
