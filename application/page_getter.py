import logging
import time
from typing import List

import pandas as pd
from PySide6.QtCore import QObject, Signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from application import config
from application.parser import Parser
from application.models import ResponseDataFrame

logger = logging.getLogger('file_logger')


class PageGetter(QObject):

    finished = Signal(ResponseDataFrame)
    message = Signal(str)

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def run(self):
        logger.debug('Catalogue processing started')
        df = self.parse_catalogue_pages_to_df()
        logger.debug('Catalogue processing finished')
        self.finished.emit(ResponseDataFrame(df=df, response_id='Catalogue'))

    def parse_catalogue_pages_to_df(self, start_page=-1, last_page=-1) -> pd.DataFrame:
        self.message.emit(f'Парсинг каталогу почато')
        self.message.emit(f'Авторизація на сайті постачальника')
        self._check_url()
        self.message.emit(f'Авторизацію пройдено')

        if config.test_mode & (start_page == -1):
            start_page, last_page = 1, 5

        list_of_pages_sources = self.parse_catalogue_pages(start_page=start_page, last_page=last_page)
        list_of_parsed_dfs = list(map(lambda x: Parser.get_table_from_the_page(x), list_of_pages_sources))
        return pd.concat(list_of_parsed_dfs)

    def parse_catalogue_pages(self, start_page=-1, last_page=-1) -> List[str]:
        if start_page == -1:
            start_page, last_page = self._get_pages_range()

        logger.info(f'Pages to parse: {start_page} - {last_page}')
        self.message.emit(f'Сторінки для парсингу: {str(start_page)} - {str(last_page)}')

        if start_page < 0:
            raise ValueError('Improper start page value')

        return self._get_pages(start_page, last_page)

    def _get_pages_range(self):
        self._check_url()
        self.driver.get(config.catalogue_url)
        return Parser.get_pages_range(self.driver.page_source)

    def _get_pages(self, start_page: int, finish_page: int) -> List[str]:
        result_list = []
        for page_number in range(start_page, finish_page + 1):
            self.message.emit(f'Парсинг сторінки {page_number}')
            if page_number == 0:
                url = config.catalogue_url
            else:
                url = f'{config.catalogue_url}?page={page_number}'
            result_list.append(self._get_page(url))
        return result_list

    def _check_url(self):
        if 'catalog' not in self.driver.current_url:
            self._login()

    def _login(self):
        try:
            self.driver.get(config.login_url)
            login = self.driver.find_element(By.NAME, "email")
            password = self.driver.find_element(By.NAME, "password")
            submit_button = self.driver.find_element(By.CLASS_NAME, 'btn-primary')
            login.send_keys(config.login)
            password.send_keys(config.password)
            submit_button.click()
            time.sleep(config.time_delay)
            self.driver.get(config.catalogue_url)
        except Exception as ex:
            pass

    def _get_page(self, url: str) -> str:
        self.driver.get(url)
        time.sleep(config.time_delay)
        return self.driver.page_source

    @staticmethod
    def create_the_driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        path_to_driver = config.assets_dir / 'chromedriver.exe'
        logger.debug(path_to_driver)
        return webdriver.Chrome(executable_path=str(path_to_driver),
                                options=chrome_options)





