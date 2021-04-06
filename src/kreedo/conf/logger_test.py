import logging
from kreedo.conf.logger import CustomFormatter


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)


# # A string with a variable at the "info" level
logger.warning("Logger test Called")
