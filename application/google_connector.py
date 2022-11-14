from .core import Singleton
import pathlib
import pygsheets as pgs
from application import config
import pandas as pd
from typing import NoReturn


class GoogleConnector(metaclass=Singleton):
    _schema = {}

    def __init__(self):
        try:
            self.client = pgs.authorize(client_secret=self._get_credentials_dir() / 'client_secret.json',
                                        credentials_directory=self._get_credentials_dir())
            self.sh = self.client.open(config.google_table_name)
            self.ws = self.sh.worksheet('title', config.sheet_to_sync_name)
            self._processing_columns = [config.code_sync_column,
                                        config.supplier_code_sync_column,
                                        config.availability_sync_column,
                                        config.price_sync_column]
        except Exception as ex:
            print(f'Exception occurs: {ex}')

    @staticmethod
    def _get_credentials_dir() -> pathlib.Path:
        return pathlib.Path(__file__).parents[1].resolve() / 'assets'

    def get_table_into_df(self) -> pd.DataFrame:
        df = self.ws.get_as_df(end=f'AF{self.ws.rows}', numerize=True)
        columns_numbers = [(k, v) for v, k in enumerate(df.columns.to_list())]
        GoogleConnector._schema = dict(filter(lambda x: x[0] in self._processing_columns, columns_numbers))
        df = df[self._processing_columns]
        return self._format_google_df(df)

    @classmethod
    def _format_google_df(cls, df):
        df[config.supplier_code_sync_column] = df[config.supplier_code_sync_column].astype('str')
        df = cls._filter_google_table_by_supplier_prefix(df)
        df[config.price_sync_column].fillna(0, inplace=True)
        df[config.price_sync_column] = df[config.price_sync_column].apply(lambda x: x if x != '' else 0.0)
        df['Код_поставщика'] = df[config.supplier_code_sync_column].apply(lambda x:
                                                                          x[len(config.supplier_prefix) + 1:])
        df.reset_index(inplace=True, drop=False, names=['row_number'])
        df.drop(inplace=True, columns=['filter_mask'])
        return df

    def save_changes_into_gsheet(self, data: pd.DataFrame) -> NoReturn:
        pass

    @staticmethod
    def _filter_google_table_by_supplier_prefix(data: pd.DataFrame) -> pd.DataFrame:
        data['filter_mask'] = data[config.supplier_code_sync_column]\
            .apply(lambda x: x[:2] == config.supplier_prefix)
        return data.loc[data['filter_mask']].copy()

