import logging
from datetime import datetime
from typing import Union
from scrapyscript import Job, Processor

import pandas as pd
from PySide6 import QtWidgets as qw
from PySide6.QtCore import Slot, QThread, QThreadPool
from scrapy.crawler import CrawlerRunner
from scrapy.signals import spider_closed
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from application.google_connector import GoogleConnector
from application.main_window import Ui_MainWindow
from application.page_getter import ScrapyPageGetter
from application.synchronizer import Synchronizer
from application.crawler_process import QtCrawlerProcess


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

        self.google_df: Union[None, pd.DataFrame] = None
        self.catalogue_df: Union[None, pd.DataFrame] = None

        self.ui.pushButton_2.clicked.connect(self._run_sync)
        self.ui.pushButton.clicked.connect(self.close)

        self.logger = logging.getLogger('app_logger')
        logging.getLogger('app_logger').setLevel(logging.DEBUG)

        self.start_time = None

    def _run_sync(self):
        # self.ui.pushButton_2.setDisabled(True)
        self.start_time = datetime.now()
        self._show_message('Синхронізацію запущено')

        logging.getLogger('scrapy').propagate = False
        the_job = Job(ScrapyPageGetter)
        processor = Processor(settings=None)
        data = processor.run(the_job)
        print(data)
        print('Scrapy process finished!')

        # scrapy_crawler_qt_process = QtCrawlerProcess()
        # pool = QThreadPool.globalInstance()
        # pool.start(scrapy_crawler_qt_process)

    @Slot(str)
    def _show_message(self, message_str: str) -> None:
        self.ui.textBrowser.append(f'{message_str}')

    @Slot(int, int)
    def _page_range(self, n1: int, n2: int) -> None:
        self.ui.textBrowser.append(f'Діапазон сторінок {n1}-{n2} роспізнано')

    @Slot(int)
    def _page_processed(self, n: int):
        self.ui.textBrowser.append(f'Сторінку {n} роспізнано')

    @Slot()
    def _logged_in(self):
        self.ui.textBrowser.append(f'Авторизацію здійснено')

    def spider_ended(self):
        # reactor.stop()
        print('Ended')
        self.ui.pushButton_2.setDisabled(False)
        return

        self.catalogue_df = None
        self.google_df = GoogleConnector().get_the_df()

        if (self.google_df is not None) and (self.catalogue_df is not None):
            df_to_google_table = Synchronizer.sync_tables(self.catalogue_df, self.google_df)
            GoogleConnector.save_changes_into_gsheet(df_to_google_table)
            self._show_message('Синхронізацію закінчено')
            td = datetime.now() - self.start_time
            self._show_message(f'Час синхронизації: {(td.seconds // 60)} мін {td.seconds % 60} с')
        else:
            if self.google_df is None:
                self.ui.textBrowser.append(f'Помилка синхронизації. Немає Google таблиці')
            elif self.catalogue_df is None:
                self.ui.textBrowser.append(f'Помилка синхронизації. Немає таблиці каталогу')
            else:
                self.ui.textBrowser.append(f'Помилка синхронизації. Інша помилка')













