from unittest import TestCase

import pandas as pd

from application.page_getter import PageGetter


class TestGetAndParse(TestCase):

    def test_get_and_parse(self):
        actual = PageGetter.parse_catalogue_pages_to_df(start_page=2, last_page=4)
        self.assertTrue(isinstance(actual, pd.DataFrame))
        self.assertEqual(60, actual.shape[0])
        actual.to_pickle('pickled_sample_table.pickle')
