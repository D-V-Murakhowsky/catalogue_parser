from unittest import TestCase

import pandas as pd

from application.synchronizer import Synchronizer


class TestReadWriteExcel(TestCase):

    def setUp(self) -> None:
        self.google_table = pd.read_pickle('google_table.pickle')
        self.site_table = pd.read_pickle('pickled_sample_table.pickle').reset_index(drop=True)

    def test_excel_read_write(self):
        Synchronizer._new_articles_to_excel(self.google_table, self.site_table)
