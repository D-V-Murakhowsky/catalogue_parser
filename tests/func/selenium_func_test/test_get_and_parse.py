from unittest import TestCase

import pandas as pd

from application.page_getter import PageGetter
from application.run_the_sync import SyncRunner


class TestGetAndParse(TestCase):

    def setUp(self) -> None:
        self.driver = SyncRunner._create_the_driver()

    def test_get_and_parse(self):
        actual = PageGetter(self.driver).parse_catalogue_pages_to_df(start_page=2, last_page=4)
        self.assertTrue(isinstance(actual, pd.DataFrame))
        self.assertEqual(60, actual.shape[0])
