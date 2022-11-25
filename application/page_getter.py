import pandas as pd
from PySide6.QtCore import Signal, QObject
from scrapy import Spider
from scrapy.http import FormRequest, Request

from application import config
from application.parser import Parser


class ScrapySignals(QObject):
    page = Signal(int)
    page_range = Signal(int, int)
    logged_in = Signal()

    def __getitem__(self, item):
        return self


class ScrapyPageGetter(Spider):

    _signals = ScrapySignals()

    name = 'spartak_sample_spider'
    start_urls = [config.login_url]
    allowed_domains = ["b2b.spartakelectronics.com"]
    df_list = []

    @property
    def df(self):
        return pd.concat(self.df_list)

    def parse(self, response):
        yield FormRequest.from_response(response=response, formid='login',
                                        formdata={'email': config.login,
                                                  'password': config.password},
                                        callback=self.logged_in)

    def logged_in(self, response):
        if response.url == 'http://b2b.spartakelectronics.com/ru/dashboard':
            self._signals.logged_in.emit()
            yield Request(url=config.catalogue_url, callback=self.get_pages_range)

    def get_pages_range(self, response):
        if response.url == config.catalogue_url:
            start_page, last_page = Parser.get_pages_range(response.text)
            self._signals.page_range.emit(start_page, last_page)
            yield Request(url=config.catalogue_url, callback=self.get_page)
            for page_number in range(start_page + 1, 5):
                yield Request(url=f'{config.catalogue_url}?page={page_number}', callback=self.get_page)

    def get_page(self, response):
        self.df_list.append(Parser.get_table_from_the_page(response.text))
        self._signals.page.emit(1)







