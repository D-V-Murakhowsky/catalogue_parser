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

    @property
    def google_table_name(self):
        return self.data['google_table']

    @property
    def sheet_to_sync_name(self):
        return self.data['sheet_name']

    @property
    def price_sync_column(self):
        return self.data['price_sync']

    @property
    def supplier_code_sync_column(self):
        return self.data['supplier_code_sync']

    @property
    def code_sync_column(self):
        return self.data['code_sync']

    @property
    def availability_sync_column(self):
        return self.data['availability_sync']

    @property
    def supplier_prefix(self):
        return self.data['prefix']

    def __init__(self):
        filepath = pathlib.Path(__file__).parents[1].resolve() / 'assets/data.json'
        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)['spartakelectronics.com']

