
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

from apps.api.views import UrlsViewSet, VideosViewSet, ConverterViewSet


router = routers.DefaultRouter()
router.register('urlset', UrlsViewSet)

urlpatterns = [
    # Custom Routers
    path('', include(router.urls)),
    
    # Rest Routers
    path('auth/', include('rest_framework.urls')),

    # v1 API
    path("v1/videos/", VideosViewSet.as_view()),
    path('v1/converter/', ConverterViewSet.as_view()),
]
