import logging
from typing import NoReturn

import pandas as pd
from PySide6.QtCore import QObject, Signal

from application import config
from application.models import ResponseDataFrame

EXCEL_COLUMNS = ['Код_поставщика', 'Наименование', 'Цена', 'Ссылки на изображения', 'Флаг_добавления']


logger = logging.getLogger('file_logger')


class Synchronizer(QObject):
    finished = Signal(ResponseDataFrame)
    message = Signal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('file_logger')

    def sync_tables(self, supplier_data: pd.DataFrame, google_sheet_data: pd.DataFrame) -> NoReturn:
        """
        Make changes in google table data, read and write excel data
        :return: updated dataframe with changes in google data
        """
        self.logger.debug('Synchronization started')
        self.logger.debug(f'Catalogue dataframe shape {supplier_data.shape}')
        self.logger.debug(f'Google dataframe shape {google_sheet_data.shape}')
        self.message.emit('Почато синхронізацію отриманих даних')

        existing_articles = \
            supplier_data.loc[supplier_data['article'].isin(google_sheet_data['Код_поставщика'].values)]

        self._new_articles_to_excel(google_sheet_data, supplier_data)

        if existing_articles.shape[0] > 0:
            df = self._change_data_in_google_table(google_sheet_data, existing_articles)

            self.logger.debug(f'Add data dataframe shape {df.shape}')
        else:
            df = pd.DataFrame()
            self.logger.debug('No articles to synchronize')
            self.message.emit('Рядкі для синхронизації відсутні')

        self.finished.emit(ResponseDataFrame(df=df, response_id='GoogleWrite'))

    @classmethod
    def _new_articles_to_excel(cls, google_sheet_data, supplier_data) -> NoReturn:
        """
        Choose data to write into the Excel table
        :param google_sheet_data: dataframe with data from the Google sheet
        :param supplier_data: dataframe with data from the supplier's site
        :return: None
        """
        excel_df = cls._read_excel()
        not_existing_present_articles = \
            supplier_data.loc[~supplier_data['article'].isin(google_sheet_data['Код_поставщика'].values)]
        not_existing_present_articles = \
            not_existing_present_articles.loc[not_existing_present_articles.quantities > 0]
        not_existing_present_articles = \
            not_existing_present_articles.loc[
                ~not_existing_present_articles['article'].isin(excel_df['Код_поставщика'])]
        not_existing_present_articles.drop(columns=['quantities'], inplace=True)
        not_existing_present_articles.rename(columns={'names': 'Наименование',
                                                      'article': 'Код_поставщика',
                                                      'prices': 'Цена',
                                                      'images': 'Ссылки на изображения'},
                                             inplace=True)
        not_existing_present_articles['Флаг_добавления'] = '-'
        excel_df = pd.concat([excel_df, not_existing_present_articles]).reset_index(drop=True)
        cls._write_excel(excel_df)

    @classmethod
    def _change_data_in_google_table(cls, google_df: pd.DataFrame, supplier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Updates data in the dataframe with data from the google table
        :param google_df: dataframe with data from the google sheet
        :param supplier_df: dataframe with data from the supplier's site
        :return:
        """
        google_df['change_flag'] = False
        for index, row in google_df.iterrows():
            try:
                syncing = supplier_df.loc[supplier_df['article'] == row['Код_поставщика']]
                if syncing.shape[0] > 0:
                    supplier_data = syncing.iloc[0]
                else:
                    continue
            except Exception as ex:
                logger.error(f'Exception occurred during syncro process. Error message {ex}')

            if row[config.price_sync_column] != supplier_data['prices']:
                google_df.at[index, config.price_sync_column] = supplier_data['prices']
                google_df.at[index, 'change_flag'] = True

            if (row[config.availability_sync_column] == '+') & (supplier_data['quantities'] <= 0):
                google_df.at[index, config.availability_sync_column] = '-'
                google_df.at[index, 'change_flag'] = True

            if (row[config.availability_sync_column] == '-') & (supplier_data['quantities'] > 0):
                google_df.at[index, config.availability_sync_column] = '+'
                google_df.at[index, 'change_flag'] = True
        return google_df

    @staticmethod
    def _read_excel() -> NoReturn:
        """
        Reads Excel file
        :return: None
        """
        try:
            if (path := config.assets_dir / config.excel_file_name).exists():
                return pd.read_excel(path, index_col=0, header=0, converters={'Код_поставщика': str})
            else:
                return pd.DataFrame(columns=EXCEL_COLUMNS)
        except Exception as ex:
            logger.error(f'Error while reading Excel. Error message: {ex}')

    @staticmethod
    def _write_excel(df: pd.DataFrame) -> NoReturn:
        """
        Writes excel file
        :param df: data to write
        :return: None
        """
        try:
            df.to_excel(config.assets_dir / config.excel_file_name)
        except Exception as ex:
            logger.error(f'Error while writing Excel. Error message: {ex}')

