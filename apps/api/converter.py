from youtube_dl import YoutubeDL

from apps.api.models import VideosModel, UrlsModel
from apps.api.helper import dicto

from apps.api.exceptions import ReturnNoneReference
from urllib.parse import urlparse

from pprint import pprint

class YoutubeConverter (object):
    def __init__(self):
        self.ydl_opts = {
            'cachedir': False,
            'forceurl':True
        }


        self.output_data = {
            'url' : ''
        }

    def convert (self, selected_url,selected_format,selected_quality):
        extracted_data = self.__get_video_data(url=selected_url)
        
        self.__set_output_data(
            extracted_data,
            selected_format,
            selected_quality
        )

        self.__store_video_data(extracted_data)


    def __get_video_data (self, url, download=False):
        if url == None:
            return None
        else:
            video_url = urlparse(url).query.replace("v=","")
            already_exists = VideosModel.objects.filter(uid=video_url).exists()

            if not already_exists:
                # process video
                ydl = YoutubeDL(self.ydl_opts)
                ydl.cache.remove()
                
                soup = ydl.extract_info(url, download=download)
            else:
                video_object = None
                video_query = VideosModel.objects.filter(uid=video_url)
                if video_query:
                    video_object = video_query[0]

            data = {
                'uid'     : soup.get('id')          if not already_exists else video_object.uid,
                'url'     : soup.get('webpage_url') if not already_exists else video_object.url,
                'title'   : soup.get('title')       if not already_exists else video_object.title,
                'uploader': soup.get('uploader')    if not already_exists else video_object.uploader,
                'views'   : soup.get('view_count')  if not already_exists else video_object.views_count,

                'thumbs'  : {
                    'low' : soup.get('thumbnails')[0].get('url')    if not already_exists else video_object.thumbs.low_url,
                    'med' : soup.get('thumbnails')[1].get('url')    if not already_exists else video_object.thumbs.med_url,
                    'high': soup.get('thumbnails')[-2].get('url')   if not already_exists else video_object.thumbs.high_url,
                    'max' : soup.get('thumbnails')[-1].get('url')   if not already_exists else video_object.thumbs.max_url,
                },

                'audios'  : {
                    'low' : soup.get('formats')[0].get('url') if not already_exists else video_object.audios.low_url,
                    'med' : soup.get('formats')[1].get('url') if not already_exists else video_object.audios.med_url,
                    'high': soup.get('formats')[2].get('url') if not already_exists else video_object.audios.high_url,
                    'max' : soup.get('formats')[3].get('url') if not already_exists else video_object.audios.max_url,
                },

                'videos'  : {
                    'low' : soup.get('formats')[-4].get('url') if not already_exists else video_object.videos.low_url,
                    'med' : soup.get('formats')[-3].get('url') if not already_exists else video_object.videos.med_url,
                    'high': soup.get('formats')[-2].get('url') if not already_exists else video_object.videos.high_url,
                    'max' : soup.get('formats')[-1].get('url') if not already_exists else video_object.videos.max_url,
                }
            }

            return data

    def __store_video_data (self, data):

        if data:
            self.data = dicto(data)
            already_exists = VideosModel.objects.filter(uid=self.data.uid).exists()

            if not already_exists:
                video_object = VideosModel()

                video_object.uid         = self.data.uid
                video_object.url         = self.data.url
                video_object.title       = self.data.title
                video_object.uploader    = self.data.uploader
                video_object.views_count = self.data.views

                thumbs = UrlsModel()
                thumbs.uid      = self.data.uid
                thumbs.low_url  = self.data.thumbs.low
                thumbs.med_url  = self.data.thumbs.med
                thumbs.high_url = self.data.thumbs.high
                thumbs.max_url  = self.data.thumbs.max
                thumbs.save()
                video_object.thumbs = thumbs

                audios = UrlsModel()
                audios.uid      = self.data.uid
                audios.low_url  = self.data.audios.low
                audios.med_url  = self.data.audios.med
                audios.high_url = self.data.audios.high
                audios.max_url  = self.data.audios.max
                audios.save()
                video_object.audios = audios

                videos = UrlsModel()
                videos.uid      = self.data.uid
                videos.low_url  = self.data.videos.low
                videos.med_url  = self.data.videos.med
                videos.high_url = self.data.videos.high
                videos.max_url  = self.data.videos.max
                videos.save()
                video_object.videos = videos

                video_object.save()
            else:
                video_object = VideosModel.objects.get(uid=self.data.uid)
                video_object.save()


    def __set_output_data (self, data, _format, quality):
        if data == None:
            raise ReturnNoneReference("Params not send in request")

        urls = data.get(_format)
        url = urls.get(quality)

        self.output_data.update({
            'url' : url
        })
