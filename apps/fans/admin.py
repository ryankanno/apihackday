from django.contrib import admin
from fans.models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subscription, SubscriptionAdmin)
