import logging.handlers
import time
from logging import LogRecord


class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):

    def __init__(self,
                 filename,
                 when='h',
                 interval=1,
                 backupCount=0,
                 encoding=None,
                 delay=False,
                 utc=False,
                 atTime=None):
        super().__init__(
            # filename + time.strftime('%Y%m%d%H%M', time.localtime()) + ".log",
            filename,
            when,
            interval,
            backupCount,
            encoding,
            delay,
            utc,
            atTime)
        super().setFormatter(logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s][%(lineno)s]: %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            style='%'
        ))

    def emit(self, record: LogRecord) -> None:
        super().emit(record)


