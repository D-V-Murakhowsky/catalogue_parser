from unittest import TestCase
import pathlib

class TestUpdateGoogle(TestCase):

    def setUp(self) -> None:
        path = pathlib.Path(__file__).parent.resolve() / 'updated_google_df.pickle'
        self.df = pd.read_pickle(path)