import time
from typing import List

from selenium.webdriver.common.by import By

from application import config
from application.selenium_connector import driver


class PageGetter:

    @classmethod
    def get_pages(cls, start_page: int, finish_page: int) -> List[str]:
        result_list = []
        for page_number in range(start_page, finish_page):
            if page_number == 0:
                url = config.catalogue_url
            else:
                url = f'{config.catalogue_url}?page={page_number - 1}'
            result_list.append(cls._get_page(url))
        return result_list

    @staticmethod
    def _login(cls):
        try:
            driver.get(config.login_url)
            login = driver.find_element(By.NAME, "email")
            password = driver.find_element(By.NAME, "password")
            submit_button = driver.find_element(By.CLASS_NAME, 'btn-primary')
            login.send_keys(config.login)
            password.send_keys(config.password)
            submit_button.click()
        except Exception as ex:
            pass

    @staticmethod
    def _get_page(url: str) -> str:
        driver.get(url)
        time.sleep(5)
        return driver.page_source





