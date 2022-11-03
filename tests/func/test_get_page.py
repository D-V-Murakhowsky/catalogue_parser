from unittest import TestCase

from application.selenium_connector.page_getter import PageGetter


class TestGetPage(TestCase):

    def test_parse_first_sheet(self):
        try:
            PageGetter.login()
            text = PageGetter.get_page(0)
            self.assertLess(0, len(text))
        except Exception as ex:
            self.assertTrue(False)
