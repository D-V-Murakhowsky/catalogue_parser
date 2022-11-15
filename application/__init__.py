from .conf import Config
import logging

logger = logging.getLogger('app_logger')
file_logger = logging.getLogger('file_logger')
fh = logging.FileHandler('log.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
file_logger.addHandler(fh)
file_logger.setLevel(logging.DEBUG)
file_logger.debug('Log started')

config = Config()
