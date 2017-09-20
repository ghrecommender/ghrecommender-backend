from django.contrib.auth import get_user_model

from rest_framework import serializers
from social_django.models import UserSocialAuth

from recommendations.utils import get_stars
from subscriptions.models import Subscription

__all__ = ['UserSerializer', 'UserSocialSerializer']


class UserSocialSerializer(serializers.ModelSerializer):
    extra_data = serializers.DictField()

    class Meta:
        model = UserSocialAuth
        fields = ('id', 'extra_data')


class UserSerializer(serializers.ModelSerializer):
    social_auth = UserSocialSerializer(read_only=True, many=True)
    stars = serializers.SerializerMethodField()
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'social_auth', 'stars', 'subscribed',)

    @staticmethod
    def get_stars(user):
        return get_stars(user.username)

    @staticmethod
    def get_subscribed(user):
        sub, created = Subscription.objects.get_or_create(user=user)
        return sub.status
