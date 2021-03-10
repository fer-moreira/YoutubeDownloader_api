from django.db import models
from datetime import datetime, timezone, timedelta
import timeago


class BaseModel (models.Model):
    id = models.AutoField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')


    @property
    def updated_at_no_utc (self):
        return self.updated_at.replace(tzinfo=None)

    @property
    def created_timeago (self):
        try:
            __now = datetime.now()
            __updated = self.updated_at_no_utc
            __date = __now - __updated
            __timeago = timeago.format(__date)

            return __timeago
        except Exception as r:
            return "long time ago"


class UrlsModel (BaseModel):
    uid = models.CharField(
        max_length=300, 
        unique=False,
        verbose_name="Video Unique ID"
    )

    low_url  = models.TextField(verbose_name="Low quality Element URL")
    med_url  = models.TextField(verbose_name="Med quality Element URL")
    high_url = models.TextField(verbose_name="High quality Element URL")
    max_url  = models.TextField(verbose_name="Max quality Element URL")

    def __str__(self):
        return str(self.uid)

class VideosModel (BaseModel):
    uid = models.CharField(
        max_length=300, 
        unique=True, 
        verbose_name="UID"
    )
    
    url = models.URLField(
        verbose_name="URL"
    )
    title = models.CharField(
        max_length=300,
        verbose_name="Title"
    )

    uploader = models.CharField(
        max_length=300, 
        verbose_name="Uploader"
    )
    views_count = models.IntegerField(
        verbose_name="Views"
    )

    thumbs = models.ForeignKey(UrlsModel,related_name='thumbs', verbose_name="Thumbs List", on_delete=models.CASCADE)
    audios = models.ForeignKey(UrlsModel,related_name='audios', verbose_name="Audios List", on_delete=models.CASCADE)
    videos = models.ForeignKey(UrlsModel,related_name='videos', verbose_name="Videos List", on_delete=models.CASCADE)

    @property
    def updated_at_no_utc (self):
        return self.updated_at.replace(tzinfo=None)

    @property
    def created_timeago (self):
        try:
            __now = datetime.now()
            __updated = self.updated_at_no_utc
            __date = __now - __updated
            __timeago = timeago.format(__date)

            return __timeago
        except Exception as r:
            return "long time ago"



    def __str__(self):
        return str("{0} | {1}".format(self.uid, self.title))