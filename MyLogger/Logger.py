import json
import os
import logging.config
import logging

# check if logging.json has been loaded
if not logging.root.handlers:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    with open('logging.json') as f:
        data = json.load(f)
        print(data)
    # read initial config file
    logging.config.dictConfig(config=data)
    # CustomConfig(config=data)
    # # create and start listener on port 9999
    # t = logging.config.listen(int(os.getenv('PORT')))
    # t.start()
#     log = logging.getLogger(__name__)
# else:
#     log = logging.getLogger(__name__)


def getLogger(name: str):
    return logging.getLogger(name)

