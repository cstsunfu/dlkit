import logging
import os
import colorlog


class logger(object):
    """docstring for logger"""
    global_logger = None
    global_log_file = None
    global_file_handler = None
    global_log_file = None
    color_config = {
        'DEBUG': 'white',  # cyan white
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(self, log_file: str='', base_dir: str='logs', log_level: str='debug', log_name='dlk'):
        super(logger, self).__init__()
        self.log_file = log_file
        self.base_dir = base_dir
        if self.base_dir and not os.path.isdir(self.base_dir):
            os.mkdir(self.base_dir)

        self.init_global_logger(log_level=log_level, log_name=log_name)
        self.init_file_logger(log_file, base_dir, log_level=log_level)

    @staticmethod
    def get_logger()->logging.Logger:
        """TODO: Docstring for get_logger.
        :returns: TODO

        """
        if logger.global_logger is None:
            logger.init_global_logger()
            logger.global_logger.warning("You didn't init the logger, so we use the default logger setting to output to terminal, you can always set the file logger by yourself.")
        return logger.global_logger

    @staticmethod
    def init_file_logger(log_file, base_dir='logs', log_level: str='debug'):
        """TODO: Docstring for init_file_logger.
        :log_file: TODO
        :base_dir: TODO
        :log_level: TODO
        :returns: TODO
        """
        if log_file:
            log_file = os.path.join(base_dir, log_file)
        if log_file and log_file != logger.global_log_file:
            if logger.global_file_handler is not None:
                logger.global_logger.removeHandler(logger.global_file_handler)
            file_handler = logging.FileHandler(filename=log_file, mode='a', encoding='utf8')
            file_handler.setLevel(logger.level_map[log_level])

            file_formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                                                      datefmt='%m/%d/%Y %H:%M:%S')
            file_handler.setFormatter(file_formatter)
            logger.global_file_handler = file_handler
            logger.global_logger.addHandler(file_handler)

    @staticmethod
    def init_global_logger(log_level: str='debug', log_name: str='dlk'):
        """TODO: Docstring for init_global_logger.
        :returns: TODO
        """
        if logger.global_logger is None:
            logger.global_logger = logging.getLogger(log_name)
            logger.global_logger.setLevel(logger.level_map[log_level])
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logger.level_map[log_level])
            console_formatter = colorlog.ColoredFormatter(
                fmt='%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                datefmt='%m/%d/%Y %H:%M:%S',
                log_colors=logger.color_config)
            console_handler.setFormatter(console_formatter)
            logger.global_logger.addHandler(console_handler)