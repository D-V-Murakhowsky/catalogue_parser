import pathlib
from unittest import TestCase

import pandas as pd

from application.parser import Parser


class TestPageParsing(TestCase):

    def setUp(self) -> None:
        path = pathlib.Path(__file__).parent.resolve() / 'source.txt'
        with open(path, encoding='utf-8') as f:
            self.text = f.read()
        self.df = pd.read_pickle('pickled_sample_table.pickle')

    def test_page(self):
        result = Parser.get_table_from_the_page(self.text)
        self.assertLess(0, result.shape[0])

    def test_page_cleaner(self):
        cleaned_df = Parser.proceed_articles_table(self.df)
        pass
