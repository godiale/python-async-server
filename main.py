import logging.config
import yaml
import pathlib


def init_logging(filename):
    with open('logger.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    config['handlers']['file']['filename'] = f'log/{filename}'
    pathlib.Path('log').mkdir(exist_ok=True)
    logging.config.dictConfig(config)


def print_hi(name):
    logger.info(f'Hi, {name}')


if __name__ == '__main__':
    init_logging(filename='main.log')
    logger = logging.getLogger(__name__)

    print_hi('PyCharm')
