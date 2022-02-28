import requests
from urllib.parse import urlencode
import time

from tinder_api import user as u
from tinder_api.utils import config as c
from tinder_api.utils import request_handlers as r


class Session:
    def __init__(self):
        self.id = self.get_id()

    @staticmethod
    def get_profile(include: (list, None) = None) -> requests.models.Response:
        url = '/v2/profile'

        if not include:
            include = [
                'account', 'available_descriptors', 'boost', 'bouncerbypass', 'contact_cards',
                'email_settings', 'instagram', 'likes', 'profile_meter', 'notifications',
                'misc_merchandising', 'offerings', 'plus_control', 'purchase', 'readreceipts',
                'spotify', 'super_likes', 'tinder_u', 'travel', 'tutorials', 'user'
            ]

        params = urlencode({
            'locale': 'ru-RU',
            'include': ','.join(include)
        })

        url += '?' + params

        return r.get(url)

    @staticmethod
    def get_meta(v=2):
        """ Returns meta information """
        url = '/v2/meta' if v == 2 else '/meta'

        resp = r.get(url)

        return resp

    @staticmethod
    def get_id():
        """ Returns the _id of the Session """
        return r.get('/profile')['_id']

    @staticmethod
    def me():
        """ Returns a UserModel() for the Session """
        return u.UserController(r.get('/profile')['_id']).get_user()

    @staticmethod
    def yield_users():
        """ Returns a generator of nearby users as NormalUser() """
        while True:
            resp = r.get('/user/recs')
            recs = resp['results'] if 'results' in resp else []
            for rec in recs:
                yield u.UserController(rec['_id']).get_user()

    @staticmethod
    def yield_usersv2():
        """ Returns a generator of nearby users as NormalUser() and calculates location """
        while True:
            resp = r.get('/v2/recs/core?locale=ru-RU')
            recs = resp['data']['results'] if 'data' in resp else []
            for rec in recs:
                if rec['type'] == 'user':
                    yield u.UserController(rec['user']['_id']).get_user()

    @staticmethod
    def yield_matches():
        """Returns a generator of matches as MatchUsers()"""
        resp = r.post('/updates', {'last_activity_date': ''})
        for match in reversed(resp['matches']):
            yield u.UserController(match['_id']).get_user()

    @staticmethod
    def list_matches() -> list:
        """ Returns a [] of matches """
        return r.post('/updates', {'last_activity_date': ''})['matches']

    @staticmethod
    def get_updates(date='') -> requests.models.Response:
        """ Returns the profile 'updates' since date
        Date formatting is specific:
            date = '2022-02-27T21:03:08.000Z"
            if date='' then returns updates since profile was made
        """
        return r.post('/updates', {'last_activity_date': date})

    @staticmethod
    def fast_match_count() -> int:
        """ Returns the number of like's the session user has received """
        return r.get('/v2/fast-match/count')['data']['count']

    @staticmethod
    def fast_match_img() -> bytes:
        """ Returns the blurred image thumbnails of users in fast-match, TinderGold """
        return requests.get('/v2/fast-match/preview', headers=c.headers).content

    @staticmethod
    def get_likes(page_token=None) -> requests.models.Response:
        """ Returns a [] of my likes """
        url = '/v2/my-likes?locale=ru-RU'
        if page_token:
            url += f'&page_token={page_token}'

        return r.get(url)

    @staticmethod
    def get_all_likes(page_token=None) -> []:
        """ Returns a [] of all my likes """
        all_likes = []

        while True:
            resp = Session.get_likes(page_token=page_token)

            data = resp.get('data')

            if not data:
                break

            likes = data.get('results', [])
            if likes and type(likes) == list:
                all_likes = all_likes + likes

            page_token = data.get('page_token')

            if page_token:
                time.sleep(0.5)
            else:
                break

        return all_likes
