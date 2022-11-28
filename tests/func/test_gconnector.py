from unittest import TestCase

from application.google_connector import GoogleConnector


class TestGoogleConnector(TestCase):

    def setUp(self) -> None:
        self.g_connector = GoogleConnector()

    def test_get_and_filter_df(self):
        self.assertIsNotNone(self.g_connector.get_the_df())
