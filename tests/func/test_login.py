from unittest import TestCase

from application.selenium_connector.page_getter import PageGetter


class TestLogin(TestCase):

    def test_login(self):
        PageGetter.login()
