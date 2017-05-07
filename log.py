from constants import *
import logging
import sys
from __future__ import print_function
# Logger to use everywhere
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(LOGGER)
print = logger.info