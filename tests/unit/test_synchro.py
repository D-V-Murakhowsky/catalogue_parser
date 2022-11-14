from unittest import TestCase

import pandas as pd

from application.synchronizer import Synchronizer


class TestComparator(TestCase):

    def setUp(self) -> None:
        self.google_table = pd.read_pickle('google_table.pickle')
        self.site_table = pd.read_pickle('pickled_sample_table.pickle')

    def test_comparator(self):
        Synchronizer.sync_tables(self.site_table, self.google_table)