#
# This module is used to handle errors and exceptions.
#

from tools import Logger
from tools import Timer

# This class is used to handle errors and exceptions.
class ErrorHandlers:
    def __init__(self):
        pass

    # This method is used to handle errors and exceptions.
    def handle_error(self, error_message):
        Logger.log_error(error_message)
        Timer.sleep(1)
        exit(1)