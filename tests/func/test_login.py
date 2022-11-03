from unittest import TestCase

from application.selenium_connector.page_getter import PageGetter


class TestLogin(TestCase):

    def test_logging_and_get_on_first_page(self):
        try:
            PageGetter.login()
            text = PageGetter.get_page(0)
            self.assertLess(0, len(text))
        except Exception as ex:
            self.assertTrue(False)
