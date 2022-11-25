from scrapy.http import FormRequest, Request
from application import config
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from application.parser import Parser


class SpiderSample(Spider):

    name = 'spartak_sample_spider'
    start_urls = [config.login_url]
    allowed_domains = ["b2b.spartakelectronics.com"]

    def parse(self, response):
        print('Parse start')
        yield FormRequest.from_response(response=response, formid='login',
                                    formdata={'email': config.login,
                                              'password': config.password},
                                        callback=self.logged_in)

    def logged_in(self, response):
        print('Logged in')
        if response.url == 'http://b2b.spartakelectronics.com/ru/dashboard':
            yield Request(url=config.catalogue_url, callback=self.get_pages_range)

    def get_pages_range(self, response):
        print('Pages range')
        if response.url == config.catalogue_url:
            start_page, last_page = Parser.get_pages_range(response.text)
            yield Request(url=config.catalogue_url, callback=self.get_page)
            for page_number in range(start_page + 1, 10):
                yield Request(url=f'{config.catalogue_url}?page={page_number}', callback=self.get_page)

    def get_page(self, response):
        print(response.url)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SpiderSample)
    process.start()