from unittest import TestCase

import pandas as pd

from application.synchronizer import Synchronizer


class TestComparator(TestCase):

    def setUp(self) -> None:
        self.google_table = pd.read_pickle('google_table.pickle')
        self.site_table = pd.read_pickle('pickled_sample_table.pickle').reset_index(drop=True)

    def test_read_excel(self):
        pass

    def test_write_excel(self):
        pass

    def test_comparator(self):
        self.site_table.at[49, 'article'] = '6896'
        Synchronizer.sync_tables(self.site_table, self.google_table)