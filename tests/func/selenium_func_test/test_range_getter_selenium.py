from unittest import TestCase

from application.page_getter import PageGetter


class TestPageRange(TestCase):

    def test_page_range(self):
        actual = PageGetter._get_pages_range()
        self.assertEqual(1, actual[0])
        self.assertTrue(actual[0] <= actual[1])