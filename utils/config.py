from dotenv import load_dotenv
import os

load_dotenv()


def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0


BOT_CONFIG = {
    'TIMEOUT': convert_to_int(os.getenv('TIMEOUT')),
    'DEVMAN_TOKEN': os.getenv('DEVMAN_TOKEN'),
    'DEVMAN_URL': os.getenv('DEVMAN_URL'),
    'TELEGRAM_TOKEN': os.getenv('TELEGRAM_TOKEN'),
    'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID'),
}
