from rest_framework import views
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

from .serializers import UserSerializer
from .utils import UserKeyConstructor

__all__ = ['UserView']


class UserView(views.APIView):
    @cache_response(key_func=UserKeyConstructor())
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
