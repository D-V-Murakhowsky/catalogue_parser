import logging

from PySide6 import QtWidgets as qw
from PySide6.QtCore import Slot, QThreadPool

from application.main_window import Ui_MainWindow
from application.run_the_sync import SyncRunner


class TheWindow(qw.QMainWindow):
    """
    Program's graphic interface
    """

    def __init__(self):
        """
        Main window constructor
        """
        # main window init
        super(TheWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self._run_sync)
        self.ui.pushButton.clicked.connect(self.close)

        self.logger = logging.getLogger('app_logger')
        logging.getLogger('app_logger').setLevel(logging.DEBUG)

    def _run_sync(self):
        self.ui.pushButton_2.setDisabled(True)
        synchronizer = SyncRunner()
        synchronizer.signal.message_signal.connect(self._show_message)
        synchronizer.signal.finish_signal.connect(self._enable_button)
        QThreadPool().start(synchronizer)

    @Slot(str)
    def _show_message(self, message_str: str) -> None:
        self.ui.textBrowser.append(f'{message_str}')

    @Slot()
    def _enable_button(self):
        self._show_message('Синхронізацію закінчено')
        self.ui.pushButton_2.setDisabled(False)











