import sys
import json

import requests
import telegram
from telegram.error import TelegramError

from devman.api import DevmanApi
from utils.logger_config import get_logger
from utils.config import Config

logger = get_logger(__file__)


def get_result_of_examination_attempt(attempt_data):
    lesson_title = attempt_data['lesson_title']
    title_response = f'Your task {lesson_title} has been examinated.'

    if attempt_data['is_negative']:
        body_response = 'Unfortunately, examinator had found some errors.'
    else:
        body_response = 'You can go ahead with a next task.'

    return f'{title_response}\n{body_response}'


def run_devman_long_polling(devman_api, telegram_bot, telegram_chat_id):
    timestamp = None

    while True:

        try:
            devman_response = devman_api.request(timestamp)
        except (requests.Timeout, requests.ConnectionError) as e:
            logger.error(f'An error occurred during connection to remote server: {str(e)}')
            continue

        try:
            devman_json_content = devman_response.json()
        except json.JSONDecodeError as e:
            logger.info(f'Cannot parse response from remote server : {str(e)}.')
            continue

        try:

            timestamp = devman_json_content.get('timestamp_to_request', None) or timestamp
            examination_attempts = devman_json_content.get('new_attempts', None)

            logger.info(f'New timestamp has been recorded: {timestamp}.')

            if not examination_attempts:
                logger.info('No new attempts were found.')
                continue

            for attempt in examination_attempts:
                message_to_notificate = get_result_of_examination_attempt(attempt)
                telegram_bot.send_message(
                    chat_id=telegram_chat_id, text=message_to_notificate
                )

        except KeyError as e:
            logger.error(f'An error occurred during reading attributes of response: {str(e)}')
            continue
        except TelegramError as e:
            logger.error(f'An error occurred during connection to telegram: {str(e)}')
            continue


def main():
    errors = []
    for key in Config.required:
        if not getattr(Config, key):
            errors.append(f'Environment variable {key} has not been configured properly.')
    if errors:
        error_message = '\n'.join(errors)
        sys.stdout.write(error_message)
        sys.exit(1)

    logger.info('Application has started.')

    devman_api = DevmanApi(
        Config.DEVMAN_URL, Config.DEVMAN_TOKEN, Config.TIMEOUT
    )

    logger.info('Devman API object has been initialized correctly.')

    telegram_bot = telegram.Bot(token=Config.TELEGRAM_BOT_TOKEN)

    logger.info('Telegram bot has been initialized correctly.')

    run_devman_long_polling(devman_api, telegram_bot, Config.TELEGRAM_CHAT_ID)


if __name__ == '__main__':
    main()
