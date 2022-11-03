from unittest import TestCase

from application.parser import Parser


class TestPageParsing(TestCase):

    def setUp(self) -> None:
        with open('source.txt', encoding='utf-8') as f:
            self.text = f.read()

    def test_page(self):
        result = Parser.recognize_page(self.text)
        self.assertLess(0, result.shape[0])
