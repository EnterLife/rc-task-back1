import logging
import os
import configparser

class Logger:
    def __init__(self, log_file, log_level):
        self.log_file = log_file
        self.log_level = log_level

    def configure_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        formatter_rh = logging.Formatter(
            '%(asctime)s [%(levelname)s] [pid: %(process)d] [%(name)s]' 
            '(%(filename)s).%(funcName)s(%(lineno)d)\n'
            '%(message)s\n'
        )
        formatter_ch = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        rh = logging.FileHandler(self.log_file, delay=True)
        ch = logging.StreamHandler()

        if self.log_level == 'debug':
            rh.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            rh.setLevel(logging.WARNING)
            ch.setLevel(logging.INFO)

        rh.setFormatter(formatter_rh)
        ch.setFormatter(formatter_ch)

        logger.addHandler(ch)
        logger.addHandler(rh)

        return logger


def get_current_directory(file):
    return os.path.dirname(os.path.abspath(file))


def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    return config


def get_logger(logger_name):
    current_dir = get_current_directory(__file__)
    log_path = current_dir
    log_name = 'log.txt'

    config = read_config(current_dir + "\\" + "settings.ini")
    log_level = 'debug' if config.getboolean("Logging", "debug") else 'info'

    logger = Logger(log_path + '\\' + log_name, log_level)
    return logger.configure_logger(logger_name)
