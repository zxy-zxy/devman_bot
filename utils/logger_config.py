import sys
import logging

import telegram

from utils.config import BOT_CONFIG

FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')


class TelegramHandler(logging.Handler):
    def __init__(self, telegram_token, telegram_chat_id):
        super().__init__()
        self._bot = telegram.Bot(
            token=telegram_token)
        self._telegram_chat_id = telegram_chat_id

    def emit(self, record):
        formatted_record = self.format(record)
        self._bot.send_message(
            chat_id=self._telegram_chat_id,
            text=formatted_record
        )


def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def _get_telegram_handler():
    telegram_handler = TelegramHandler(
        BOT_CONFIG['TELEGRAM_LOGGER_BOT_TOKEN'],
        BOT_CONFIG['TELEGRAM_CHAT_ID'])
    telegram_handler.setFormatter(FORMATTER)
    return telegram_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_console_handler())
    logger.addHandler(_get_telegram_handler())
    logger.propagate = False
    return logger
