from django.db import models
from itertools import chain

class SubscriptionManager(models.Manager):

    def notify(self, league_id=None, team_id=None, game_id=None):

        league_subs = self.filter(league_id=league_id) if league_id else self.none()
        team_subs   = self.filter(team_id=team_id) if team_id else self.none()
        game_subs   = self.filter(game_id=game_id) if game_id else self.none()

        return list(chain(league_subs, team_subs, game_subs))


    def get_active_subs_by_user(self, user):
        return self.filter(status=self.model.ACTIVE, created_by=user.id)


    def get_league_subs(self, user, league_ids=None):
        user_subs = self.get_active_subs_by_user(user)

        if league_ids is None:
            return user_subs.filter(league_id__isnull=False, team_id__isnull=True,
                game_id__isnull=True) 
        else:
            return user_subs.filter(league_id__in=league_ids, team_id__isnull=True, 
                game_id__isnull=True)


    def get_team_subs(self, user, league_id=None, team_id=None):
        user_subs = self.get_active_subs_by_user(user)

        if league_id is None and team_id is None:
            return user_subs.filter(league_id__isnull=False, team_id__isnull=False, 
                game_id__isnull=True)
        else:
            return user_subs.filter(league_id=league_id, team_id=team_id, 
                game_id__isnull=True)


    def get_game_subs(self, user, game_ids=None):
        user_subs = self.get_active_subs_by_user(user)

        if game_ids is None:
            return user_subs.filter(game_id__isnull=False)
        else:
            return user_subs.filter(game_id__in=game_ids)
