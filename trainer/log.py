from __future__ import print_function
import logging
from constants import *
import sys
# Logger to use everywhere
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(LOGGER)
print = logger.info
