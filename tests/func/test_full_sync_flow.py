from unittest import TestCase

from application.page_getter import PageGetter
from application.run_the_sync import SyncRunner
from application.google_connector import GoogleConnector
from application.synchronizer import Synchronizer


class TestFullFlow(TestCase):

    def setUp(self) -> None:
        self.driver = SyncRunner._create_the_driver()
        self.page_getter = PageGetter(self.driver)
        self.google_connector = GoogleConnector()

    def test_full_flow(self):
        catalogue_df = self.page_getter.parse_catalogue_pages_to_df(signal=None)
        google_df = self.google_connector.get_table_into_df()
        data_for_update = Synchronizer.sync_tables(supplier_data=catalogue_df,
                                                   google_sheet_data=google_df)
        self.google_connector.save_changes_into_gsheet(data_for_update)

