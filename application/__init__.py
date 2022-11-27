from .conf import Config
import logging
from scrapy.utils.log import configure_logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('app_logger')
file_logger = logging.getLogger('file_logger')
file_logger.propagate = False
fh = logging.FileHandler('log.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
file_logger.addHandler(fh)
file_logger.setLevel(logging.DEBUG)
file_logger.debug('Log started')

configure_logging(settings={"LOG_ENABLED": False})

config = Config()
