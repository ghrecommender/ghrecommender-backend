from django.contrib.auth.models import User
from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from social_django.models import UserSocialAuth

expected_recommendations = [
    {'name': 'matplotlib/basemap', 'score': 1, 'description': 'description'},
    {'name': 'jswhit/basemap', 'score': 0.9, 'description': 'description'},
    {'name': 'funkaster/cocos2d-x', 'score': 0.8, 'description': 'description'},
]


class RecommendationsAPITest(APITestCase):
    url = reverse('api-recommendations')

    def setUp(self):
        self.user = User.objects.create_user(
            username='example',
            email='user@example.com',
            password='examplepassword',
        )
        UserSocialAuth.objects.create(
            user=self.user,
            uid=123,
            extra_data={'login': 'example'},
        )

    def test_get_recommendations_not_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('recommendations.views.get_recommendations')
    def test_get_recommendations(self, mock_get_recommendations):
        mock_get_recommendations.return_value = expected_recommendations
        self.client.login(username='example', password='examplepassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_recommendations)
