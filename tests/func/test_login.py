from unittest import TestCase

from application.selenium_connector.parser import Parser


class TestLogin(TestCase):

    def test_login(self):
        Parser.login()

    def test_parse_first_sheet(self):
        Parser.login()
        Parser.get_page(0)
