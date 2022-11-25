import json
import logging
import os
import pathlib


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

    @property
    def excel_file_name(self):
        return self.data['excel_file']

    @property
    def test_mode(self):
        return self.data['test_mode'] == 1

    @property
    def google_secret(self):
        return self.data['google_secret']

    @property
    def assets_dir(self):
        return self.cwd / 'assets'

    def __init__(self):
        self.cwd = pathlib.Path(str(os.getcwd())).resolve()
        filepath = self.cwd / 'assets/data.json'
        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)['spartakelectronics.com']
        logging.getLogger('file_logger').debug('JSON loaded')

