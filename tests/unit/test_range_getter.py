import pathlib
from unittest import TestCase

from application.parser import Parser


class TestPageRange(TestCase):
    def setUp(self) -> None:
        path = pathlib.Path(__file__).parent.resolve() / 'source.txt'
        with open(path, encoding='utf-8') as f:
            self.text = f.read()

    def test_page_range_getter(self):
        actual = Parser.get_pages_range(self.text)
        self.assertEqual((1, 306), actual)