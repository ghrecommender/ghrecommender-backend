import json
from functools import partial
from operator import itemgetter

from django.conf import settings

import requests
from pymongo import MongoClient


mongo = MongoClient(settings.MONGO_HOST, 27017)
users = mongo.gh.users
repositories = mongo.gh.projects


def recommend(user_id, count=10, popular=False):
    """
    >>> recommend(33132, count=3)
    [[19603496, 0.926357880234718], [28043157, 0.90995229780674], [31913264, 0.885282531380653]]
    """
    payload = {
        "method": "recommend",
        "params": [user_id, count, popular],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(settings.RPC_MODEL_URL,
                             data=json.dumps(payload)).json()
    return response.get('result', [])


def get_repositories(ids):
    """
    >>> get_repositories([3, 4, 5])
    [{'_id': 3, 'url': 'matplotlib/basemap', 'description': 'description'},
     {'_id': 4, 'url': 'jswhit/basemap', 'description': 'description'},
     {'_id': 5, 'url': 'funkaster/cocos2d-x', 'description': 'description'}]
    """
    return repositories.find({
        '_id': {
            '$in': list(ids),
        }
    })


def merge(raw_items_by_id, item):
    """
    >>> item = {'_id': 3, 'url': 'matplotlib/basemap', 'description': 'description'}
    >>> raw_items_by_id = {3: 0.9, 4: 0.8, 5: 0.7}
    >>> merge(raw_items_by_id, item)
    {
        "url": "",
        "description": "description",
        "score": 0.9
    }
    """
    score = raw_items_by_id[item['_id']]
    return dict(
        name=item['url'],
        description=item['description'],
        score=score,
    )


def prepare_recommendations(raw_recommendations):
    """
    >>> raw_recommendations = [[19603496, 0.926357880234718], 
                               [28043157, 0.90995229780674], 
                               [31913264, 0.885282531380653]]
    >>> prepare_recommendations(raw_recommendations)
    [{'name': 'matplotlib/basemap', 'score': 1, 'description': 'description'},
     {'name': 'jswhit/basemap', 'score': 0.9, 'description': 'description'},
     {'name': 'funkaster/cocos2d-x', 'score': 0.8, 'description': 'description'}]
    """
    raw_items_by_id = {item_id: score for item_id,
                       score in raw_recommendations}
    ids = raw_items_by_id.keys()
    repos = get_repositories(ids)
    return map(partial(merge, raw_items_by_id), repos)


def get_user(gh_login):
    """
    >>> get_user("yurtaev")
    {
        '_id': 325598,
        'login': 'yurtaev',
        'stars': 538,
    }
    """
    return users.find_one({'login': gh_login})


def get_stars(gh_login):
    """
    >>> get_stars("yurtaev")
    538
    """
    user = get_user(gh_login)
    return user.get('stars') if user else None


def get_raw_user_id(gh_login):
    """
    >>> get_raw_user_id("yurtaev")
    325598
    """
    user = get_user(gh_login)
    if user:
        return user['_id']
    return None


def get_raw_recommendations(gh_login, count=10, popular=False):
    """
    >>> get_raw_recommendations("yurtaev", count=3)
    [[3, 1], [4, 0.9], [5, 0.8]]
    """
    user_id = get_raw_user_id(gh_login)
    return recommend(user_id, count=count, popular=popular)


def get_recommendations(gh_login, count=10, popular=False):
    """
    >>> get_recommendations("yurtaev", count=3)
    [{'name': 'matplotlib/basemap', 'score': 1, 'description': 'description'},
     {'name': 'jswhit/basemap', 'score': 0.9, 'description': 'description'},
     {'name': 'funkaster/cocos2d-x', 'score': 0.8, 'description': 'description'}]
    """
    raw_recommendations = get_raw_recommendations(gh_login, count=count, popular=popular)
    data = prepare_recommendations(raw_recommendations)
    return sorted(data, key=itemgetter('score'), reverse=True)
