import os


def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None


class Config:
    required = [
        'DEVMAN_TOKEN',
        'DEVMAN_URL',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_LOGGER_BOT_TOKEN',
        'TELEGRAM_CHAT_ID'
    ]

    TIMEOUT = convert_to_int(os.getenv('TIMEOUT'))
    DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')
    DEVMAN_URL = os.getenv('DEVMAN_URL')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_LOGGER_BOT_TOKEN = os.getenv('TELEGRAM_LOGGER_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
