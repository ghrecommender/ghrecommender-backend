from django.db import models
from django.conf import settings

from django_extensions.db.models import TimeStampedModel


class Subscription(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='subscription')
    status = models.BooleanField(default=False, db_index=True)
