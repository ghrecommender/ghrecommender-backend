from django.test import TestCase
from mock import patch

from recommendations.utils import get_recommendations, prepare_recommendations


raw_recommendations = [
    [3, 1],
    [4, 0.9],
    [5, 0.8]
]

expected_recommendations = [
    {'name': 'matplotlib/basemap', 'score': 1, 'description': 'description'},
    {'name': 'jswhit/basemap', 'score': 0.9, 'description': 'description'},
    {'name': 'funkaster/cocos2d-x', 'score': 0.8, 'description': 'description'},
]

projects_mongo = [{'_id': 3, 'url': 'matplotlib/basemap', 'description': 'description'},
                  {'_id': 4, 'url': 'jswhit/basemap', 'description': 'description'},
                  {'_id': 5, 'url': 'funkaster/cocos2d-x', 'description': 'description'}]


class UtilsTestCase(TestCase):
    @patch('recommendations.utils.get_repositories')
    @patch('recommendations.utils.get_raw_recommendations')
    def test_get_recommendations(self, mock_get_raw_recommendations, mock_get_repositories):
        mock_get_raw_recommendations.return_value = raw_recommendations
        mock_get_repositories.return_value = projects_mongo
        data = get_recommendations('yurtaev')
        self.assertListEqual(data, expected_recommendations)

    @patch('recommendations.utils.get_repositories')
    def test_prepare_recommendations(self, mock_get_repositories):
        mock_get_repositories.return_value = projects_mongo

        data = prepare_recommendations(raw_recommendations)

        expected_data = [{'name': 'matplotlib/basemap', 'score': 1, 'description': 'description'},
                         {'name': 'jswhit/basemap', 'score': 0.9, 'description': 'description'},
                         {'name': 'funkaster/cocos2d-x', 'score': 0.8, 'description': 'description'}]
        self.assertListEqual(list(data), expected_data)
