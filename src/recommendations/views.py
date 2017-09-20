from rest_framework import views
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

from recommendations.serializers import RecommendationSerializer
from core.utils import UserKeyConstructor

from .utils import get_stars, get_recommendations

__all__ = ['RecommendationsView']


class RecommendationsView(views.APIView):
    @cache_response(key_func=UserKeyConstructor())
    def get(self, request):
        username = request.user.username
        popular = get_stars(username) <= 30
        recommendations = get_recommendations(username, count=100, popular=popular)
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
