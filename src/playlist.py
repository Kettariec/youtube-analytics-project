import os
import requests
from googleapiclient.discovery import build
import isodate
import datetime


class PlayList:
    """класс для плейлиста"""
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    url_pl = 'https://www.youtube.com/playlist?list='
    url_video = 'https://youtu.be/'

    def __init__(self, id_playlist):
        self.__id_playlist = id_playlist
        self.title = self.channel_info()['items'][0]['snippet']['title']
        self.url = self.url_pl + self.__id_playlist

    def channel_info(self):
        """Метод для получения информации
        о канале по id плейлиста"""
        info = requests.get(
            f'https://www.googleapis.com/youtube/v3/playlists?key='
            f'{self.api_key}&id={self.__id_playlist}'
            f'&part=id,snippet&fields='
            f'items(id,snippet(title,channelId,channelTitle))')
        return info.json()

    def pl_response(self):
        """Метод для получения информации о плейлисте"""
        pl_video = self.youtube.playlistItems().list(
            playlistId=self.__id_playlist, part='contentDetails',
            maxResults=50).execute()
        return pl_video

    @property
    def total_duration(self):
        """Метод, который считает
        суммарную длительность плейлиста"""
        video_ids = [video['contentDetails']['videoId']
                     for video in self.pl_response()['items']]
        video_response = self.youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)).execute()
        total_time = datetime.timedelta(0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time

    @staticmethod
    def like_count(video_id):
        """Метод для получения количества лайков видео"""
        video = PlayList.youtube.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=video_id).execute()
        likes = video['items'][0]['statistics']['likeCount']
        return int(likes)

    def show_best_video(self):
        """Метод для получения ссылки на видео,
        с наибольшим количеством лайков"""
        id_video = ''
        best_likes = 0
        for video in self.pl_response()['items']:
            likes = self.like_count(video['contentDetails']['videoId'])
            if likes > best_likes:
                id_video = video['contentDetails']['videoId']
        return self.url_video + id_video
