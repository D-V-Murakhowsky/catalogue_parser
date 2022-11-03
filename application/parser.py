from bs4 import BeautifulSoup
import pandas as pd


class Parser:

    @staticmethod
    def recognize_page(source: str) -> pd.DataFrame:
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