from .core import Singleton
import pathlib
import pygsheets as pgs
from application import config
import pandas as pd
from typing import NoReturn


class GoogleConnector(metaclass=Singleton):

    def __init__(self):
        try:
            self.client = pgs.authorize(client_secret=self._get_credentials_dir() / 'client_secret.json',
                                        credentials_directory=self._get_credentials_dir())
            self.sh = self.client.open(config.google_table_name)
            self.ws = self.sh.worksheet('title', config.sheet_to_sync_name)
        except Exception as ex:
            print(f'Exception occurs: {ex}')

    @staticmethod
    def _get_credentials_dir() -> pathlib.Path:
        return pathlib.Path(__file__).parents[1].resolve() / 'assets'

    def get_table_into_df(self) -> pd.DataFrame:
        df = self.ws.get_as_df(end=f'AF{self.ws.rows}', numerize=False)
        df = df[[config.code_sync_column, config.supplier_code_sync_column,
                 config.availability_sync_column, config.price_sync_column]]
        df = self._filter_google_table_by_supplier_prefix(df)
        return df.drop(columns=['filter_mask'])

    def save_changes_into_gsheet(self, data: pd.DataFrame) -> NoReturn:
        pass

    @staticmethod
    def _filter_google_table_by_supplier_prefix(data: pd.DataFrame) -> pd.DataFrame:
        data['filter_mask'] = data[config.supplier_code_sync_column]\
            .apply(lambda x: x[:2] == config.supplier_prefix)
        return data.loc[data['filter_mask']].copy()

