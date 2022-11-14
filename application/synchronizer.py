import pathlib
from typing import NoReturn

import pandas as pd

from application import config

EXCEL_COLUMNS = ['Код_поставщика', 'Наименование', 'Цена', 'Флаг_добавления']


class Synchronizer:

    @classmethod
    def sync_tables(cls,
                    supplier_data: pd.DataFrame,
                    google_sheet_data: pd.DataFrame) -> pd.DataFrame:

        existing_articles = \
            supplier_data.loc[supplier_data['article'].isin(google_sheet_data['Код_поставщика'].values)]
        excel_df = cls._read_excel()

        not_existing_present_articles = cls._new_articles_to_excel(excel_df, google_sheet_data, supplier_data)
        excel_df = pd.concat([excel_df, not_existing_present_articles])
        cls._write_excel(excel_df)
        return existing_articles

    @classmethod
    def _new_articles_to_excel(cls, excel_df, google_sheet_data, supplier_data):
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
                                                      'prices': 'Цена'},
                                             inplace=True)
        not_existing_present_articles['Флаг_добавления'] = '-'
        return not_existing_present_articles

    @staticmethod
    def _read_excel():
        if (path := pathlib.Path(__file__).parents[1].resolve() / f'assets/{config.excel_file_name}').exists():
            return pd.read_excel(path)
        else:
            return pd.DataFrame(columns=EXCEL_COLUMNS)

    @staticmethod
    def _write_excel(df: pd.DataFrame) -> NoReturn:
        df.to_excel(pathlib.Path(__file__).parents[1].resolve() / f'assets/{config.excel_file_name}')
