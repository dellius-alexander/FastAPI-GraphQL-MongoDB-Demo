import logging
from typing import Literal


class CustomFormatter(logging.Formatter):
    """Custom Logging Formatter"""

    # Colors for log levels
    colors = {
        'DEBUG': '\033[1;36m',  # cyan
        'INFO': '\033[1;32m',  # green
        'WARNING': '\033[1;33m',  # yellow
        'ERROR': '\033[1;31m',  # red
        'CRITICAL': '\033[1;35m',  # magenta
    }

    def __init__(self, format=None, datefmt=None, style: Literal['%'] = '%'):
        # Overriding the 'format' method of the logging.Formatter class
        logging.Formatter.__init__(self, fmt=format, datefmt=datefmt, style=style)

    def format(self, record: logging.LogRecord):
        """Format the log message
        :param record: the log record
        :return: the formatted log message
        """
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
        return '%s%s\033[1;0m' % (self.colors[level_name], msg)

    def format_record(self, record: logging.LogRecord):
        """Format the log record and return the formatted record
        :param record: the log record
        :return: the formatted log record
        """
        record.msg = self.format(record)
        return record

