from rest_framework import serializers


class RecommendationSerializer(serializers.Serializer):
    name = serializers.CharField()
    score = serializers.FloatField()
    description = serializers.CharField()
