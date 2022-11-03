from bs4 import BeautifulSoup
import pandas as pd
from typing import Tuple
import re


class Parser:

    @staticmethod
    def get_table_from_the_page(source: str) -> pd.DataFrame:
        soup = BeautifulSoup(source, 'lxml')
        table = soup.find('table')
        name, art, price, qty = [], [], [], []
        for row in table.findAll('tr')[1:]:
            col = row.findAll('td')
            if len(col) == 7:
                name.append(col[1].getText().strip())
                art.append(col[3].getText().strip())
                price.append(col[4].getText().strip())
                qty.append(col[5].getText().strip())
        return pd.DataFrame({'names': name, 'article': art, 'prices': price, 'quantities': qty})

    @staticmethod
    def get_pages_range(source: str) -> Tuple:
        soup = BeautifulSoup(source, 'lxml')
        first = list(soup.find('ul', class_='pagination').children)[2].text
        last = list(soup.find('ul', class_='pagination').children)[-3].text
        return int(first), int(last)

    @classmethod
    def proceed_articles_table(cls, df: pd.DataFrame) -> pd.DataFrame:
        df['prices'] = df['prices'].apply(cls._process_price)
        df['quantities'] = df['quantities'].apply(cls._process_qty)
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


