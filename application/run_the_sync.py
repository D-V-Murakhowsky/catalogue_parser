from PySide6.QtCore import Signal, QRunnable, Slot, QObject, QTimer

from application.selenium_connector.page_getter import PageGetter


class Signals(QObject):
    message_signal = Signal(str)
    finish_signal = Signal()


class SyncRunner(QRunnable):

    def __init__(self):
        super().__init__()
        self.signal = Signals()
        self.page_getter = PageGetter()

    def run(self):
        self.signal.message_signal.emit('Синхронізацію запущено')
        parsed_df = self.page_getter.parse_catalogue_pages_to_df(signal=self.signal.message_signal)
        self.signal.message_signal.emit('Синхронізацію завершено')


    @Slot(str)
    def status_receiver(self, message_str: str) -> None:
        self.signal.message_signal.emit(message_str)