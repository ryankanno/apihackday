from django.utils.translation import ugettext_lazy as _
from django.db import models
from utilities.db.fields import CreatedDateTimeField, ModifiedDateTimeField
from django.contrib.auth.models import User

# Create your models here.
from fans.managers import SubscriptionManager

class Subscription(models.Model):

    id          = models.BigIntegerField(editable=False, primary_key=True)
    name        = models.CharField(max_length=128, null=False, blank=False)

    league_id   = models.CharField(max_length=40, null=True, blank=False)
    team_id     = models.CharField(max_length=40, null=True, blank=False)
    game_id     = models.CharField(max_length=40, null=True, blank=False)

    objects     = SubscriptionManager()

    created_at  = CreatedDateTimeField(_('created'))
    created_by  = models.ForeignKey(User, 
        related_name="%(app_label)s_%(class)s_creator", null=True, blank=True,
        editable=False)

    modified_at = ModifiedDateTimeField(_('modified'))
    modified_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modifier", null=True, blank=True, editable=False)

    class Meta:
        get_latest_by = 'modified_at'
        ordering = ('-modified_at', '-created_at',)
