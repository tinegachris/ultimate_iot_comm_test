#
# This module is used for anthing logging related.
#

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

class Logger:
    def __init__(self, log_name, log_path, log_level):
        self.log_name = log_name
        self.log_path = log_path
        self.log_level = log_level
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = TimedRotatingFileHandler(os.path.join(self.log_path, self.log_name + '.log'), when='midnight', interval=1, backupCount=7)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def log(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_critical(self, message):
        self.logger.critical(message)

    def log_exception(self, message):
        self.logger.exception(message)