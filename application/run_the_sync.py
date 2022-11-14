import pathlib

from PySide6.QtCore import Signal, QRunnable, Slot, QObject
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from application.page_getter import PageGetter


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

    def run(self):
        self.signals.message_signal.emit('Синхронізацію запущено')
        google_df = self.page_getter.parse_catalogue_pages_to_df(signal=SyncRunner.signals.message_signal)
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
