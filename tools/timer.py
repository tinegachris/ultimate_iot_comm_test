#
# This module is used for anything timing related.
#

import time
from time import sleep
import datetime
import random
import string


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()