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

    def movie_details(self, tag):
        resp = requests.get(
            url=f'{self.__root_url}/title/get-details',
            headers=self.__headers,
            params={'tconst': tag}
        )
        resp.raise_for_status()
        content = json.loads(resp.content)
        return {
            'title': content.get('title'),
            'year': content.get('year'),
            'run_time': content.get('runningTimeInMinutes'),
            'poster': content.get('image').get('url')
        }

    def movie_plot(self, tag):
        resp = requests.get(
            url=f'{self.__root_url}/title/get-plots',
            headers=self.__headers,
            params={'tconst': tag}
        )
        resp.raise_for_status()
        content = json.loads(resp.content)
        return {
            'plot': content.get('plots').pop(0).get('text')
        }

    def movie_rating(self, tag):
        resp = requests.get(
            url=f'{self.__root_url}/title/get-ratings',
            headers=self.__headers,
            params={'tconst': tag}
        )
        resp.raise_for_status()
        content = json.loads(resp.content)
        print()
        return {
            'imdb_rate': content.get('rating')
        }

    def movie_thriller(self, tag):
        resp = requests.get(
            url=f'{self.__root_url}/title/get-videos',
            headers=self.__headers,
            params={'tconst': tag,
                    'region': 'US',
                    'limit': 25}
        )
        resp.raise_for_status()
        content = json.loads(resp.content)
        video_refs = [v.get('id').rsplit('/').pop()
                      for v in content.get('resource').get('videos')
                      if v.get('contentType').lower() == 'trailer']
        for ref in video_refs:
            resp = requests.get(
                url=f'{self.__root_url}/title/get-video-playback',
                headers=self.__headers,
                params={
                    'viconst': ref,
                    'region': 'US'
                }
            )
            resp.raise_for_status()
            content = json.loads(resp.content)
            for vid in content.get('resource').get('encodings'):
                if vid.get('mimeType') == 'video/mp4':
                    return {
                        'trailer': vid.get('playUrl')
                    }
        return {'trailer': None}

    def movie_factory(self, tag):
        from controllers import Movie
        if Movie.query.filter_by(tag=tag).first() is not None:
            raise SQLDuplicateException('Movie already exist')

        movie_attributes = {'tag': tag}
        movie_attributes.update(
            self.movie_details(tag)
        )
        movie_attributes.update(
            self.movie_plot(tag)
        )
        movie_attributes.update(
            self.movie_rating(tag)
        )
        movie_attributes.update(
            self.movie_thriller(tag)
        )
        return movie_attributes









