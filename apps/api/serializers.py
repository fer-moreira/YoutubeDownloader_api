from rest_framework import serializers

from apps.api.models import (UrlsModel, VideosModel)

class UrlsSerializer (serializers.ModelSerializer):
    class Meta:
        model = UrlsModel
        fields = ['uid', 'low_url', 'med_url', 'high_url', 'max_url']

class VideosSerializer (serializers.ModelSerializer):
    class Meta:
        model = VideosModel
        fields = ["uid", "title", "uploader", "views_count"]

