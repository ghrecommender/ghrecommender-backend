from mock import patch

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from social_django.models import UserSocialAuth

expected_socieal_user = {
    'extra_data': {'login': 'example'},
    'id': 1,
}

expected_user = dict(
    id=1,
    email="user@example.com",
    username="example",
    first_name="",
    last_name="",
    social_auth=[expected_socieal_user],
    stars=538,
    subscribed=False,
)


class UserAPITest(APITestCase):
    maxDiff = None
    url = reverse('api-user')

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

    def test_not_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('recommendations.utils.get_user')
    def test_get(self, mock_get_user):
        mock_get_user.return_value = dict(
            login="yurtaev", _id=325598, stars=538)
        self.client.login(username='example', password='examplepassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_user)

    @patch('recommendations.utils.get_user')
    def test_get_none_user(self, mock_get_user):
        mock_get_user.return_value = None
        self.client.login(username='example', password='examplepassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = expected_user.copy()
        expected_data.update(dict(stars=None))
        self.assertDictEqual(response.data, expected_data)
