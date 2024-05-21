import logging
import os

from const import LOG_DIRECTORY

class LoggerHelper:
    def initLogger():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'chatterdaemon.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    def disposeLogger():
        logger = logging.getLogger()

        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def deleteLogfile():
        try:
            os.remove(os.path.join(LOG_DIRECTORY, 'chatterdaemon.log'))
        except FileNotFoundError:
            pass