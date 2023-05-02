import json
import os
import time
from loguru import logger


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


class Logger(object):
    def __init__(self,log_name):
        self.log_name = log_name
        self.log_config = {
            'LOG_LEVEL': 'DEBUG',
            'Rotation': '1 week',
            'Compress': 'zip'
        }
        self.__log_init()

    def __log_init(self):
        self.log_level = self.log_config['LOG_LEVEL']
        self.rotation = self.log_config['Rotation']
        self.compression = self.log_config['Compress']
        self.log_file = self.log_name + '_' + time.strftime("%Y-%m-%d", time.localtime()) + '.log'
        self.log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs',self.log_file)
        self.logger = logger
        self.logger.add(
            self.log_path,
            serialize=True,
            rotation=self.rotation,
            compression=self.compression,
            enqueue=True,
            level=self.log_level
        )

    def info(self,msg):
        self.logger.info(msg)

    def error(self,msg):
        self.logger.error(msg)

    def warning(self,msg):
        self.logger.warning(msg)

log = Logger('genos_gpt')