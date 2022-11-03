import time

from selenium.webdriver.common.by import By

from application import config
from application.selenium_connector import driver


class PageGetter:

    def __del__(self):
        driver.quit()

    @staticmethod
    def login():
        driver.get(config.login_url)
        login = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CLASS_NAME, 'btn-primary')
        login.send_keys(config.login)
        password.send_keys(config.password)
        submit_button.click()

    @staticmethod
    def get_page(n: int) -> str:
        driver.get(config.catalogue_url)
        time.sleep(5)
        return driver.page_source
