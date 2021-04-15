import logging
from datetime import datetime


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler('scheduler.log')
# handler.setLevel(logging.DEBUG)
# handler.setFormatter(CustomFormatter())

# logger.addHandler(handler)

# logger.info(
#     "[{}] - !!!scheduler already started, DO NOTHING".format(datetime.now()))

# logger.warning("[{}] - Scheduler started!".format(datetime.now()))
# logger.debug("[{}] - Scheduler started!".format(datetime.now()))
# logger.debug("[{}] - Scheduler started!".format(datetime.now()))
