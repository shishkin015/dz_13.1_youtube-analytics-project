from googleapiclient.discovery import build
import os

API_KEY: str = os.environ.get('YT_API_KEY')


class Video:
    def __init__(self, video_id):
        self.video_id = video_id

        request = Video.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=video_id,
            key=API_KEY
        ).execute()

        self.name_video = request['items'][0]['snippet']['title']
        self.url_video = f"https://www.youtube.com/watch?v={self.video_id}&ab_channel={request['items'][0]['snippet']['channelTitle']}"
        self.view_count = request['items'][0]['statistics']['viewCount']
        self.like_count = request['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name_video

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
