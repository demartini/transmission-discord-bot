import logging
import os
from logging.handlers import RotatingFileHandler

import colorlog

logs_dir = "./logs"

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)


def setup_logging(log_file=logs_dir + "/bot.log", log_level=logging.INFO):
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Create formatter for file output
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create file handler and set level to debug
    file_handler = RotatingFileHandler(
        log_file, mode="w", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create colorized formatter for console output
    console_formatter = colorlog.ColoredFormatter(
        "%(light_black)s%(asctime)s%(reset)s - %(light_purple)s%(name)s - %(log_color)s%(levelname)s%(reset)s - %(white)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        reset=True,
        secondary_log_colors={},
        style="%",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


# Configure logging when this module is imported
logger = setup_logging()
