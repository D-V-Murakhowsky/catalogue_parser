import logging

from scrapyscript import Job, Processor
from PySide6.QtCore import QRunnable
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from application.page_getter import ScrapyPageGetter


class QtCrawlerProcess(QRunnable):

    def run(self):
        logging.getLogger('scrapy').propagate = False
        the_job = Job(ScrapyPageGetter)
        processor = Processor(settings=None)
        data = processor.run(the_job)
        print(data)
        print('Scrapy process finished!')