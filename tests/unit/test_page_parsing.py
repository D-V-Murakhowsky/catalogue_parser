import pathlib
from unittest import TestCase

import pandas as pd

from application.parser import Parser


class TestPageParsing(TestCase):

    def setUp(self) -> None:
        path = pathlib.Path(__file__).parent.resolve() / 'source.txt'
        with open(path, encoding='utf-8') as f:
            self.text = f.read()

    def test_page(self):
        result = Parser.get_table_from_the_page(self.text)
        self.assertLess(0, result.shape[0])

