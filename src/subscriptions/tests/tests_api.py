from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from subscriptions.models import Subscription


class RecommendationsAPITest(APITestCase):
    url = reverse('api-subscription')

    def setUp(self):
        self.user = User.objects.create_user(
            username='example',
            email='user@example.com',
            password='examplepassword',
        )

    def test_get_not_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_subscription(self):
        self.assertFalse(Subscription.objects.filter(user=self.user).exists())
        self.client.login(username='example', password='examplepassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"status": False})
        self.assertTrue(Subscription.objects.filter(user=self.user, status=False).exists())

    def test_post_subscription(self):
        self.assertFalse(Subscription.objects.filter(user=self.user).exists())
        self.client.login(username='example', password='examplepassword')

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"status": True})
        self.assertTrue(Subscription.objects.filter(user=self.user).exists())

        response = self.client.post(self.url)
        self.assertDictEqual(response.data, {"status": False})
        self.assertTrue(Subscription.objects.filter(user=self.user, status=False).exists())
