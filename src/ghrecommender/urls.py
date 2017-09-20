"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from core.views import UserView
from recommendations.views import RecommendationsView
from subscriptions.views import SubscriptionView


admin.site.site_title = 'GHRecommender'
admin.site.site_header = 'GHRecommender.io Administration'

urlpatterns = [
    url(r'^%s/' % settings.ADMIN_URL, admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    url(r'^api/user/$', UserView.as_view(), name='api-user'),
    url(r'^api/recommendations/$', RecommendationsView.as_view(), name='api-recommendations'),
    url(r'^api/subscription/$', SubscriptionView.as_view(), name='api-subscription'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
