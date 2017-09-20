from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created', 'modified',)
    list_filter = ('status', 'created', 'modified',)
