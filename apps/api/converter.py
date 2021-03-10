from youtube_dl import YoutubeDL

from apps.api.models import VideosModel, UrlsModel
from apps.api.helper import dicto

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
        if len(url) <= 0: return None
        else:
            # process video
            
            ydl = YoutubeDL(self.ydl_opts)
            ydl.cache.remove()
            
            soup = ydl.extract_info(url, download=download)


            data = {
                'uid'     : soup.get('id'),
                'url'     : soup.get('webpage_url'),
                'title'   : soup.get('title'),
                'uploader': soup.get('uploader'),
                'views'   : soup.get('view_count'),

                'thumbs'  : {
                    'low' : soup.get('thumbnails')[0].get('url'),
                    'med' : soup.get('thumbnails')[1].get('url'),
                    'high': soup.get('thumbnails')[-2].get('url'),
                    'max' : soup.get('thumbnails')[-1].get('url'),
                },

                'audios'  : {
                    'low' : soup.get('formats')[0].get('url'),
                    'med' : soup.get('formats')[1].get('url'),
                    'high': soup.get('formats')[2].get('url'),
                    'max' : soup.get('formats')[3].get('url'),
                },

                'videos'  : {
                    'low' : soup.get('formats')[-4].get('url'),
                    'med' : soup.get('formats')[-3].get('url'),
                    'high': soup.get('formats')[-2].get('url'),
                    'max' : soup.get('formats')[-1].get('url'),
                }
            }


            return data

        return None

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
        urls = data.get(_format)
        url = urls.get(quality)

        self.output_data.update({
            'url' : url
        })
