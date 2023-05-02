import logging.handlers
import os
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
            filename="logs/" + filename.split(".")[1] + "_" + time.strftime('%Y%m%d%H%M', time.localtime()) + "." + filename.split(".")[0],
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            utc=utc,
            atTime=atTime)
        super().setFormatter(logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s][%(lineno)s]: %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            style='%'
        ))
        print("Current Working Directory: ")
        print(os.getcwd())

    def emit(self, record: LogRecord) -> None:
        super().emit(record)




