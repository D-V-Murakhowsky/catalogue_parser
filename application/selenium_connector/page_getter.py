import time
from typing import List

import pandas as pd
from selenium.webdriver.common.by import By

from application import config
from application.selenium_connector import driver
from application.parser import Parser


class PageGetter:

    def __new__(cls, *args, **kwargs):
        cls._login()

    @classmethod
    def parse_catalogue_pages_to_df(cls, start_page=-1, last_page=-1) -> pd.DataFrame:
        cls._check_url()
        list_of_pages_sources = cls.parse_catalogue_pages(start_page=start_page, last_page=last_page)
        list_of_parsed_dfs = list(map(lambda x: Parser.get_table_from_the_page(x), list_of_pages_sources))
        return pd.concat(list_of_parsed_dfs)

    @classmethod
    def parse_catalogue_pages(cls, start_page=-1, last_page=-1) -> List[str]:
        if start_page == -1:
            start_page, last_page = cls._get_pages_range()

        if start_page < 0:
            raise ValueError('Improper start page value')

        return cls._get_pages(start_page, last_page)

    @classmethod
    def _get_pages_range(cls):
        cls._check_url()
        driver.get(config.catalogue_url)
        return Parser.get_pages_range(driver.page_source)

    @classmethod
    def _get_pages(cls, start_page: int, finish_page: int) -> List[str]:
        result_list = []
        for page_number in range(start_page, finish_page + 1):
            if page_number == 0:
                url = config.catalogue_url
            else:
                url = f'{config.catalogue_url}?page={page_number}'
            result_list.append(cls._get_page(url))
        return result_list

    @classmethod
    def _check_url(cls):
        if 'catalog' not in driver.current_url:
            cls._login()

    @staticmethod
    def _login():
        try:
            driver.get(config.login_url)
            login = driver.find_element(By.NAME, "email")
            password = driver.find_element(By.NAME, "password")
            submit_button = driver.find_element(By.CLASS_NAME, 'btn-primary')
            login.send_keys(config.login)
            password.send_keys(config.password)
            submit_button.click()
            time.sleep(config.time_delay)
            driver.get(config.catalogue_url)
        except Exception as ex:
            pass

    @staticmethod
    def _get_page(url: str) -> str:
        driver.get(url)
        time.sleep(config.time_delay)
        return driver.page_source





