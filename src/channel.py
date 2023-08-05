import json
import os

from googleapiclient.discovery import build

API_KEY = os.environ.get('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # id канала
        self.__channel_id = channel_id
        # создать специальный объект для работы с API
        youtube = Channel.get_service()

        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        # название канала
        self.title = channel['items'][0]['snippet']['title']
        # описание канала
        self.description = channel['items'][0]['snippet']['description']
        # общее количество просмотров
        self.views_count = int(channel['items'][0]['statistics']['viewCount'])
        # ссылка на канал
        self.url = "https://www.youtube.com/channel/" + self.__channel_id
        # количество подписчиков
        self.subscribers_count = int(channel['items'][0]['statistics']['subscriberCount'])
        # количество видео
        self.video_count = int(channel['items'][0]['statistics']['videoCount'])

    @property
    def channel_id(self) -> str:
        """Возвращает id канала."""
        return self.__channel_id

    def __str__(self) -> str:
        """Выводит в консоль информацию о канале."""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Возвращает сумму двух каналов."""
        result = self.subscribers_count + other.subscribers_count
        return result

    def __sub__(self, other):
        """Возвращает разность двух каналов."""
        result = self.subscribers_count - other.subscribers_count
        return result

    def __gt__(self, other):
        """Возвращает True, если количество подписчиков канала больше другого."""
        return self.subscribers_count > other.subscribers_count

    def __lt__(self, other):
        """Возвращает True, если количество подписчиков канала меньше другого."""
        return self.subscribers_count < other.subscribers_count

    def __eq__(self, other):
        """Возвращает True, если количество подписчиков канала равно другому."""
        return self.subscribers_count == other.subscribers_count

    def __ge__(self, other):
        """Возвращает True, если количество подписчиков канала больше или равно другому."""
        return self.subscribers_count >= other.subscribers_count

    def __le__(self, other):
        """Возвращает True, если количество подписчиков канала меньше или равно другому."""
        return self.subscribers_count <= other.subscribers_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = Channel.get_service()

        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
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
