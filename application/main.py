import logging
from datetime import datetime
from typing import Union

import pandas as pd
from PySide6 import QtWidgets as qw
from PySide6.QtCore import Slot
from scrapy.crawler import CrawlerRunner
from scrapy.signals import spider_closed
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

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

        self.start_time = None

    def _run_sync(self):
        self.ui.pushButton_2.setDisabled(True)
        self.start_time = datetime.now()
        self._show_message('Синхронізацію запущено')

        logging.getLogger('scrapy').propagate = False

        runner = CrawlerRunner()

        d = runner.crawl(ScrapyPageGetter)
        d.addBoth(lambda _: self.spider_ended())
        reactor.run()
        # process = CrawlerProcess(settings=get_project_settings())
        # process.crawl()
        # for crawler in process.crawlers:
        #     crawler.signals.connect(self.spider_ended, signal=spider_closed)
        #     crawler.spider._signals.page.connect(self._page_processed)
        #     crawler.spider._signals.page_range.connect(self._page_range)
        #     crawler.spider._signals.logged_in.connect(self._logged_in)
        # process.start()

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













