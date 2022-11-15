import pathlib
from typing import NoReturn, Union, Dict

import pandas as pd
import pygsheets as pgs

from application import config
from .core import Singleton


class GoogleConnector(metaclass=Singleton):
    _schema: Union[Dict, None] = None

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
            self._get_schema()
        except Exception as ex:
            print(f'Exception occurs: {ex}')

    @staticmethod
    def _get_credentials_dir() -> pathlib.Path:
        """
        Get credentials for authorization
        :return: path to credentials
        """
        return pathlib.Path(__file__).parents[1].resolve() / 'assets'

    def _get_schema(self) -> NoReturn:
        """
        Saves Google table's sheet schema (only necessary columns)
        :return: None
        """
        if GoogleConnector._schema is None:
            df = self.ws.get_as_df(end=f'AF2', numerize=True)
            columns_numbers = [(k, pgs.Address((None, v + 1), True).label) for v, k in enumerate(df.columns.to_list())]
            GoogleConnector._schema = dict(filter(lambda x: x[0] in self._processing_columns, columns_numbers))

    def get_table_into_df(self) -> pd.DataFrame:
        """
        Gets Google table's sheet into dataframe (just necessary range)
        :return:
        """
        return self._format_google_df(self.ws.get_as_df(end=f'AF{self.ws.rows}',
                                                        numerize=True)[self._processing_columns])

    @classmethod
    def _format_google_df(cls, df) -> pd.DataFrame:
        """
        Formats received dataframe
        :param df: dataframe to format
        :return: formatted dataframe
        """
        df[config.supplier_code_sync_column] = df[config.supplier_code_sync_column].astype('str')
        df = cls._filter_google_table_by_supplier_prefix(df)
        df[config.price_sync_column].fillna(0, inplace=True)
        df[config.price_sync_column] = df[config.price_sync_column].apply(lambda x: x if x != '' else 0.0)
        df['Код_поставщика'] = df[config.supplier_code_sync_column].apply(lambda x:
                                                                          x[len(config.supplier_prefix) + 1:])
        df.reset_index(inplace=True, drop=False, names=['row_number'])
        df['row_number'] += 2
        df.drop(inplace=True, columns=['filter_mask'])
        return df

    def save_changes_into_gsheet(self, data: pd.DataFrame) -> NoReturn:
        """
        Save changes to Google table's sheet
        :param data: data to save as the dataframe
        :return: None
        """
        data = data.loc[data['change_flag'] == True]
        for index, row in data.iterrows():
            try:
                self._update_cell(row['row_number'],
                                  row[config.availability_sync_column],
                                  row[config.price_sync_column])
            except Exception as ex:
                continue

    def _update_cell(self, row: int, availability: str, price: float) -> NoReturn:
        """
        Updates cells in the given row with the given values
        :param row: row to update
        :param availability: new availability flag (+/-)
        :param price: new price
        :return: None
        """
        self.ws.update_value(f'{self._schema[config.availability_sync_column]}{str(row)}',
                             availability)
        self.ws.update_value(f'{self._schema[config.price_sync_column]}{str(row)}',
                             round(price, 2))

    @staticmethod
    def _filter_google_table_by_supplier_prefix(data: pd.DataFrame) -> pd.DataFrame:
        """
        Filters dataframe with the data from the Google table by supplier's prefix stored in config
        :param data: data to filter
        :return: filtered data
        """
        data['filter_mask'] = data[config.supplier_code_sync_column]\
            .apply(lambda x: x[:2] == config.supplier_prefix)
        return data.loc[data['filter_mask']].copy()

