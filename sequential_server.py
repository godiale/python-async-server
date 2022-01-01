import logging
from logger import init_logging


def print_hi(name):
    log.info(f'Hi, {name}')


if __name__ == '__main__':
    init_logging(filename='bubu.log')
    log = logging.getLogger(__name__)
    print_hi('PyCharm')
