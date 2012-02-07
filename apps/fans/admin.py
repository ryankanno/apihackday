from django.contrib import admin
from fans.models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'modified_at', 'modified_by', 'created_at', 'created_by')
    ordering     = ('id',)
admin.site.register(Subscription, SubscriptionAdmin)
