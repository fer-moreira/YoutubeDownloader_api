from django.contrib import admin
from apps.api.models import (
    VideosModel,
    UrlsModel
)

from rest_framework.authtoken.models import Token


admin.site.site_header = "API Database"
admin.site.site_title = "API Database"
admin.site.index_title = "Administration"


@admin.register(VideosModel)
class VideosAdmin (admin.ModelAdmin):
    list_display = [
        "uid", 
        "title", 
        "uploader", 
        "views_count"
    ]


@admin.register(UrlsModel)
class URLSModelAdmin (admin.ModelAdmin):
    list_display = [
        'uid'
    ]
