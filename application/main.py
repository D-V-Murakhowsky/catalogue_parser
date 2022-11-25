import logging
from typing import Union

import pandas as pd
from PySide6 import QtWidgets as qw
from PySide6.QtCore import Slot, QThreadPool
from scrapy.crawler import CrawlerProcess
from scrapy.signals import spider_closed

from application.google_connector import GoogleConnector
from application.main_window import Ui_MainWindow
from application.page_getter import ScrapyPageGetter
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

        self.google_df: Union[None, pd.DataFrame] = None
        self.catalogue_df: Union[None, pd.DataFrame] = None

        self.ui.pushButton_2.clicked.connect(self._run_sync)
        self.ui.pushButton.clicked.connect(self.close)

        self.logger = logging.getLogger('app_logger')
        logging.getLogger('app_logger').setLevel(logging.DEBUG)

    def _run_sync(self):
        self.ui.pushButton_2.setDisabled(True)
        self._show_message('Синхронізацію запущено')

        google_getter = GoogleConnector()
        google_getter._signals._read_df.connect(self._save_the_google_table)
        QThreadPool().start(google_getter)

        process = CrawlerProcess({})
        process.crawl(ScrapyPageGetter)
        for crawler in process.crawlers:
            crawler.signals.connect(self.spider_ended, signal=spider_closed)
            crawler.spider._signals.page.connect(self._page_processed)
            crawler.spider._signals.page_range.connect(self._page_range)
            crawler.spider._signals.logged_in.connect(self._logged_in)
        process.start()


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

    @Slot(pd.DataFrame)
    def _save_the_google_table(self, df):
        self.google_df = df

    def spider_ended(self, spider, reason):
        if reason == 'finished':
            self.ui.textBrowser.append(f'Роспізнавання каталогу завершено')
        else:
            self.ui.textBrowser.append(f'Під час роспізнавання каталогу виникла помилка {reason}')
            return

        self.catalogue_df = spider.df
        if (self.google_df is not None) and (self.catalogue_df is not None):
            df_to_google_table = Synchronizer.sync_tables(self.catalogue_df, self.google_df)
            GoogleConnector.save_changes_into_gsheet(df_to_google_table)
            self._show_message('Синхронізацію закінчено')
        else:
            self.ui.textBrowser.append(f'Помилка синхронизації')

        self.ui.pushButton_2.setDisabled(False)













