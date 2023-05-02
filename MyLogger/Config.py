import json
import logging.config
import os
from typing import Union, Dict, Any


class CustomConfig(logging.config):
    concurrent_loggers = 0

    def __init__(self,
                 config: Dict[Any, Any] = None):
        super().__init__(config)

    @classmethod
    def dictConfig(cls,
                   config: Union[Dict] = json.load(open('logging.json')) if os.path.exists('logging.json') else None):

        # check if logging.json has been loaded
        if not logging.root.handlers:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            # read initial config file
            super().dictConfig(config)
            # # create and start listener on port 9999
            # t = logging.config.listen(int(os.getenv('PORT')))
            # t.start()
        #     log = logging.getLogger(__name__)
        # else:
        #     log = logging.getLogger(__name__)
