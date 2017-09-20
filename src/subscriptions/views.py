from rest_framework import views
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .models import Subscription


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class SubscriptionView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_object(self):
        obj, created = Subscription.objects.get_or_create(user=self.request.user)
        return obj

    def get(self, request):
        sub = self.get_object()
        return Response(dict(status=sub.status))

    def post(self, request):
        sub = self.get_object()
        sub.status = not sub.status
        sub.save()
        return Response(dict(status=sub.status))
