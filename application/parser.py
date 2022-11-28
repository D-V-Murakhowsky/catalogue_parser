from bs4 import BeautifulSoup
import pandas as pd
from typing import Tuple
import re

from application import config


class Parser:

    @staticmethod
    def get_table_from_the_page(source: str) -> pd.DataFrame:
        soup = BeautifulSoup(source, 'lxml')
        table = soup.find('table')
        name, art, price, qty, images = [], [], [], [], []
        for row in table.findAll('tr')[1:]:
            col = row.findAll('td')
            if len(col) == 7:
                images_in_row = []
                for item_in_set in col[0].findAll('img'):
                    if (data_original_value := item_in_set.get('data-original')) is None:
                        images_in_row.append(item_in_set.get('src'))
                    else:
                        images_in_row.append(data_original_value)
                name.append(col[1].getText().strip())
                art.append(col[3].getText().strip())
                price.append(col[4].getText().strip())
                qty.append(col[5].getText().strip())
                images.append(','.join(list(map(lambda x: f'{config.host}{x}', images_in_row))))
        return Parser._proceed_articles_table(pd.DataFrame({'names': name,
                                                            'article': art,
                                                            'prices': price,
                                                            'quantities': qty,
                                                            'images': images}))

    @staticmethod
    def get_pages_range(source: str) -> Tuple:
        soup = BeautifulSoup(source, 'lxml')
        first = list(soup.find('ul', class_='pagination').children)[2].text
        last = list(soup.find('ul', class_='pagination').children)[-3].text
        return int(first), int(last)

    @classmethod
    def _proceed_articles_table(cls, df: pd.DataFrame) -> pd.DataFrame:
        df['prices'] = df['prices'].apply(cls._process_price).astype('float32')
        df['quantities'] = df['quantities'].apply(cls._process_qty).astype('int32')
        return df

    @staticmethod
    def _process_price(data: str) -> float:
        try:
            before_point, after_point = data.split('.')
            whole = re.search(r'\d*', before_point).group(0)
            frac = re.search(r'\d*', after_point).group(0)
            return int(whole) + 0.01 * int(frac)
        except TypeError:
            return 0

    @staticmethod
    def _process_qty(data: str) -> int:
        try:
            match data.strip().lower():
                case 'есть в наличии':
                    return 999
                case 'нет в наличии':
                    return 0
                case _:
                    return int(re.search(r'\d*', data).group(0))
        except (TypeError, ValueError):
            return 0


