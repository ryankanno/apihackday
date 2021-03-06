from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import post_save
from utilities.db.fields import CreatedDateTimeField, ModifiedDateTimeField
from django.contrib.auth.models import User

# Create your models here.
from fans.managers import SubscriptionManager

class Subscription(models.Model):

    ACTIVE  = 1
    DELETED = 2

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )

    id          = models.AutoField(primary_key=True)
    league_id   = models.CharField(max_length=40, null=True, blank=False)
    team_id     = models.CharField(max_length=40, null=True, blank=False)
    game_id     = models.CharField(max_length=40, null=True, blank=False)
    status      = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

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

    def __unicode__(self):
        return "%s-%s-%s" % (self.league_id, self.team_id, self.game_id)

    def delete(self):
        self.status = self.DELETED
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=20, null=True, blank=False)
    timezone = models.CharField(max_length=32, null=True, blank=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
