import pathlib
from unittest import TestCase

from application.google_connector import GoogleConnector

import pandas as pd


class TestUpdateGoogle(TestCase):

    def setUp(self) -> None:
        path = pathlib.Path(__file__).parent.resolve() / 'updated_google_df.pickle'
        self.df = pd.read_pickle(path)
        self.df['row_number'] += 2
        self.google_connector = GoogleConnector()

    def test_google_update(self):
        self.google_connector.save_changes_into_gsheet(self.df)
