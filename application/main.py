import logging

from PySide6 import QtWidgets as qw
from PySide6.QtCore import Slot, QThread

from application.google_connector import GoogleConnector
from application.main_window import Ui_MainWindow
from application.models import ResponseDataFrame
from application.page_getter import PageGetter
from application.synchronizer import Synchronizer


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
        self.ui.pushButton.clicked.connect(self._close)

        self.catalogue_df = None
        self.google_df = None

        self.logger = logging.getLogger('file_logger')
        self.logger.debug('Selenium driver creation')
        self.driver = PageGetter.create_the_driver()
        self.logger.debug('Selenium driver created')

        self.catalogue_getter = PageGetter(self.driver)
        self.catalogue_thread = QThread(parent=self)
        self.catalogue_getter.moveToThread(self.catalogue_thread)
        self.catalogue_getter.message.connect(self._show_message)
        self.catalogue_getter.finished.connect(self._df_received)

        self.google_table_processor = GoogleConnector()
        self.google_thread = QThread(parent=self)
        self.google_table_processor.moveToThread(self.google_thread)
        self.google_table_processor.message.connect(self._show_message)
        self.google_table_processor.finished.connect(self._df_received)

        self.sync_process = Synchronizer()
        self.sync_thread = QThread(parent=self)
        self.sync_process.moveToThread(self.sync_thread)
        self.sync_process.message.connect(self._show_message)
        self.sync_process.finished.connect(self._finished_process)

        self.ui.pushButton_2.clicked.connect(self.catalogue_getter.run)
        self.ui.pushButton_2.clicked.connect(self.google_table_processor.run)
        self.ui.pushButton_2.clicked.connect(self._run_sync)

        self.catalogue_thread.start()
        self.google_thread.start()
        self.sync_thread.start()

        self.logger.debug('Main process init is complete')

    def _run_sync(self):
        self.logger.debug('"Run the sync" button is pressed')
        self.ui.pushButton_2.setDisabled(True)
        self.google_df = None
        self.catalogue_df = None

    def _close(self):
        if self.driver is not None:
            self.driver.quit()
            self.catalogue_thread.quit()
            self.google_thread.quit()
            self.sync_thread.quit()
            self.close()

    @Slot(ResponseDataFrame)
    def _df_received(self, response: ResponseDataFrame):
        if response.response_id == 'Catalogue':
            self.logger.debug('Catalogue dataframe is received')
            self.catalogue_df = response.df
        elif response.response_id == 'Google':
            self.logger.debug('Google dataframe is received')
            self.google_df = response.df
        else:
            self.logger.error('Illegal signal sender')
            raise RuntimeError('Illegal signal sender')

        if (self.catalogue_df is not None) & (self.google_df is not None):
            self.sync_process.sync_tables(self.catalogue_df, self.google_df)

    @Slot(str)
    def _show_message(self, message_str: str) -> None:
        self.ui.textBrowser.append(f'{message_str}')

    @Slot(ResponseDataFrame)
    def _finished_process(self, data: ResponseDataFrame):
        self.logger.debug(f'Writing into Google Sheet. DataFrame shape is {data.df.shape}')
        self.google_table_processor.save_changes_into_gsheet(data.df)
        self._show_message('Синхронізацію закінчено')
        self.ui.pushButton_2.setDisabled(False)
        self.logger.info('Sync is completed')











