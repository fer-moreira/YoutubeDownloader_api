from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

import json

from apps.api.models import (UrlsModel,VideosModel)
from apps.api.serializers import (UrlsSerializer, VideosSerializer)

from apps.api.converter import YoutubeConverter

from pprint import pprint

class UrlsViewSet(viewsets.ModelViewSet):
    queryset = UrlsModel.objects.all()
    serializer_class = UrlsSerializer

class VideosViewSet(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            try:
                videos_count = int(request.query_params.get('count',4))
            except AttributeError as r:
                videos_count = 4

            videos = VideosModel.objects.order_by("-updated_at")[0:videos_count]

            if len(videos) <= 0:
                return Response(data={'detail':"Videos not found"},status=404)
            else:
                _videos = []

                for video in videos:
                    _videos.append({
                        "uid" :      video.uid,
                        "title" :    video.title,
                        "uploader" : video.uploader,
                        "views" :    video.views_count,
                        "url":       video.url,
                        "thumbnail": video.thumbs.low_url,
                        'days_ago' : video.created_timeago
                    })

                data = {
                    'count': videos_count,
                    'found' : len(videos),
                    'filter' : 'recent',
                    'videos' : _videos
                }

                return Response(data,status=200)
        except Exception as r:
            return Response({'500' : str(r)},status=500)

class ConverterViewSet(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = request.query_params

        video_url       = payload.get('url');
        output_format   = payload.get('output_format');
        output_quality  = payload.get('output_quality');

        yc = YoutubeConverter()
        yc.convert(
            video_url,
            output_format,
            output_quality
        )
        converted_data = yc.output_data

        return Response(converted_data, status=200)

