import sys
import logging


def init_logging(logger, level=None):
    if not logger:
        logger = logging.getLogger('analyzer')
    logging.basicConfig()
    if not level:
        logger.setLevel(logging.INFO)
    if level == 'warning':
        logger.setLevel(logging.WARN)
    if level == 'debug':
        logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('analyzer.log')
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
