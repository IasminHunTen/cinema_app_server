import requests
import json

from .singleton import SingletonMeta
from extra_modules import SQLDuplicateException


class MovieRapidAPI(metaclass=SingletonMeta):

    def __init__(self):
        self.__root_url = 'https://imdb8.p.rapidapi.com'
        self.__headers = {
            'X-RapidAPI-Host': 'imdb8.p.rapidapi.com',
            'X-RapidAPI-Key': '12aeb9dc3cmsh773dcaa2097c953p1adfabjsn992e8f8be567'
        }

    def _make_request(self, url, method=requests.get, tag=None, headers=None, query_params=None):
        resp = method(
            url=f'{self.__root_url}/{url}',
            headers=self.__headers | (headers if headers is not None else {}),
            params=({'tconst': tag} if tag is not None else {}) | (query_params if query_params is not None else {})
        )
        resp.raise_for_status()
        return json.loads(resp.content)

    def _movie_plot(self, tag):
        content = self._make_request('/title/get-plots', tag=tag)
        return {
            'plot': content.get('plots').pop(0).get('text')
        }

    def _movie_rating(self, tag):
        content = self._make_request('/title/get-ratings', tag=tag)
        return {
            'imdb_rate': content.get('rating')
        }

    def _movie_trailer(self, tag):
        content = self._make_request('/title/get-videos', tag=tag, query_params={
            'region': 'US',
            'limit': 25
        })
        video_refs = [v.get('id').rsplit('/').pop()
                      for v in content.get('resource').get('videos')
                      if v.get('contentType').lower() == 'trailer']
        for ref in video_refs:
            resp = requests.get(
                url=f'{self.__root_url}/title/get-video-playback',
                headers=self.__headers,
                params={

                }
            )
            resp.raise_for_status()
            content = self._make_request('/title/get-video-playback', query_params={
                'viconst': ref,
                'region': 'US'
            })
            for vid in content.get('resource').get('encodings'):
                if vid.get('mimeType') == 'video/mp4':
                    return {
                        'trailer': vid.get('playUrl')
                    }
        return {'trailer': None}

    def _movie_genres(self, tag):
        return {
            'genres': self._make_request('/title/get-genres', tag=tag)
        }

    def _movie_directors(self, tag):
        content = self._make_request('/title/get-top-crew', tag=tag)
        return {
            'directors': [director.get('name') for director in content.get('directors')[:3]]
        }

    def movie_factory(self, tag):
        from controllers import Movie
        if Movie.query.filter_by(tag=tag).first() is not None:
            raise SQLDuplicateException('Movie already exist')

        return self._movie_plot(tag) | self._movie_rating(tag) | self._movie_trailer(tag) | {
            'extra_details': self._movie_genres(tag) | self._movie_directors(tag)
        }











