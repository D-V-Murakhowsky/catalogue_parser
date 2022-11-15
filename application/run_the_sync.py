import pathlib

from PySide6.QtCore import Signal, QRunnable, Slot, QObject
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from application.page_getter import PageGetter
from application.synchronizer import Synchronizer
from application.google_connector import GoogleConnector


class Signaler(QObject):
    message_signal = Signal(str)
    finish_signal = Signal()

    def __getitem__(self, item):
        return self


class SyncRunner(QRunnable):
    signals = Signaler()

    def __init__(self):
        super().__init__()
        self.driver = self._create_the_driver()
        self.page_getter = PageGetter(self.driver)
        self.google_connector = GoogleConnector()

    def run(self):
        self.signals.message_signal.emit('Синхронізацію запущено')
        catalogue_df = self.page_getter.parse_catalogue_pages_to_df(signal=SyncRunner.signals.message_signal)
        google_df = self.google_connector.get_table_into_df()
        SyncRunner.signals.message_signal.emit(f'Google таблицю завантажено')
        data_for_update = Synchronizer.sync_tables(supplier_data=catalogue_df,
                                                   google_sheet_data=google_df)
        self.google_connector.save_changes_into_gsheet(data_for_update)
        SyncRunner.signals.message_signal.emit(f'Google таблицю записано')
        self.signals.finish_signal.emit()

    @Slot(str)
    def status_receiver(self, message_str: str) -> None:
        self.signals.message_signal.emit(message_str)

    @staticmethod
    def _create_the_driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        path_to_driver = pathlib.Path(__file__).parents[1].resolve() / 'assets/chromedriver.exe'
        print(path_to_driver)
        return webdriver.Chrome(executable_path=str(path_to_driver),
                                options=chrome_options)
