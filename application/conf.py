import pathlib
import json


class Config:

    @property
    def login_url(self):
        return self.data['login_url']

    @property
    def catalogue_url(self):
        return self.data['catalogue_url']

    @property
    def login(self):
        return self.data['login']

    @property
    def password(self):
        return self.data['password']

    @property
    def time_delay(self):
        return int(self.data['delay'])

    def __init__(self):
        filepath = pathlib.Path(__file__).parents[1].resolve() / 'assets/data.json'
        with open(filepath, 'r') as f:
            self.data = json.load(f)['spartakelectronics.com']

