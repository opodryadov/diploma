import requests
import time
from itertools import chain
from pprint import pprint
import json
from urllib.parse import urlencode

vk_token = 'c10c735708047753e2d4fe35dd2f597424f99cead6bf3a2ba499eb5c64fc66161c694be0f21c69f476f45'

# OAUTH_URL = 'https://oauth.vk.com/authorize'
# OAUTH_PARAMs = {
#     'client_id': 7491008,
#     'display': 'page',
#     'scope': 'friends,groups',
#     'response_type': 'token',
#     'v': 5.107
# }
#
# print('?'.join(
#     (OAUTH_URL, urlencode(OAUTH_PARAMs))
# ))

class User:

    def __init__(self, id_user, token):
        self.token = token
        self.id_user = id_user

    def get_params(self):
        return {
            'access_token': self.token,
            'user_id': self.id_user,
            'v': 5.107,
        }

    def get_friends(self):
        gr = set(self.get_groups())
        friends_groups = []
        x = 1
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )
        for user_id in response.json()['response']['items']:
            try:
                new_user = User(user_id, vk_token)
                friends_groups.append(new_user.get_groups())
                time.sleep(0.5)
                print("\r {}".format(x), "из", len(response.json()['response']['items']), end="")
                x += 1
            except:
                x += 1
        gr_fr = set(list(chain.from_iterable(friends_groups)))
        gr.difference_update(gr_fr)
        return list(gr)

    def get_groups(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params,
        )
        return response.json()['response']['items']

    def get_group_by_id(self):
        my_gr = self.get_friends()
        my_string = ','.join(str(e) for e in my_gr)
        response = requests.get(
            'https://api.vk.com/method/groups.getById',
            {
                'access_token': self.token,
                'user_id': self.id_user,
                'v': 5.107,
                'group_ids': my_string,
                'fields': 'members_count, id, name',
                },
            )
        return response.json()


with open('groups.json', 'w', encoding='utf-8') as file:
    start = User('171691064', vk_token)
    js = start.get_group_by_id()['response']
    json.dump(js, file, ensure_ascii=False, indent=2)