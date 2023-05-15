import json
import os

from googleapiclient.discovery import build

API_KEY = os.environ.get('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        # создать специальный объект для работы с API
        youtube = Channel.get_service()

        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.views_count = channel['items'][0]['statistics']['viewCount']
        self.url = channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscribers_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = Channel.get_service()

        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube."""
        return cls.youtube

    def to_json(self):
        """Возвращает объект в формате JSON."""
        json_sample = {
            'title': self.title,
            'description': self.description,
            'views_count': self.views_count,
            'url': self.url,
            'subscribers_count': self.subscribers_count,
            'video_count': self.video_count
        }
        with open('channel.json', 'w', encoding='utf-8') as file:
            json.dump(json_sample, file, indent=2, ensure_ascii=False)
