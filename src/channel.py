import os
import json
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Атрибуты инициализируются через API
        """
        self.channel_id = channel_id
        playlists = youtube.channels().list(id=channel_id,
                                            part='snippet,statistics'
                                            ).execute()
        self.playlists = playlists
        for playlist in playlists['items']:
            self.id = playlist['id']
            self.title = playlist['snippet']['title']
            self.description = playlist['snippet']['description']
            self.url = playlist['snippet']['thumbnails']['default']['url']
            self.subscribers = int(playlist['statistics']['subscriberCount'])
            self.video_count = int(playlist['statistics']['videoCount'])
            self.views = int(playlist['statistics']['viewCount'])

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id,
                                          part='snippet,statistics'
                                          ).execute()
        print(channel)

    def to_json(self, filename) -> None:
        """Сохраняет в json-файл значения атрибутов экземпляра Channel"""
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video count": self.video_count,
            "views": self.views
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)
