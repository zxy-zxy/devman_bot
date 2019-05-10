import sys

import requests
import telegram

from devman.api import DevmanApi
from utils.logger_config import get_logger
from utils.config import BOT_CONFIG

logger = get_logger(__file__)


def get_result_of_examination_attempt(attempt_data):
    lesson_title = attempt_data['lesson_title']
    title_response = f'Your task {lesson_title} has been examinated.'

    if attempt_data['is_negative']:
        body_response = 'Unfortunately, examinator had found some errors.'
    else:
        body_response = 'You can go ahead with a next task.'

    return '\n'.join([title_response, body_response])


def run_devman_long_polling(devman_api, telegram_bot, telegram_chat_id):
    timestamp = None

    while True:

        try:

            devman_json_content = devman_api.request(timestamp)
            if devman_json_content is None:
                continue

            timestamp = devman_json_content.get('timestamp_to_request', None)
            examination_attempts = devman_json_content.get('new_attempts', None)

            logger.info(f'New timestamp has been recorded: {timestamp}.')

            if not examination_attempts:
                logger.info('No new attempts were found.')
                continue

            for attempt in examination_attempts:
                message_to_notificate = get_result_of_examination_attempt(attempt)
                telegram_bot.send_message(chat_id=telegram_chat_id, text=message_to_notificate)

        except (requests.Timeout, requests.ConnectionError) as e:
            logger.error(e)
            continue
        except (requests.HTTPError, requests.RequestException) as e:
            logger.error(e)
            break


def main():
    logger.info('Application has started.')

    has_error = False
    for key, value in BOT_CONFIG.items():
        if not BOT_CONFIG[key]:
            logger.error(f'Environment variable has not been setup properly: {key}')
            has_error = True

    if has_error:
        sys.exit(1)

    print()

    devman_api = DevmanApi(
        BOT_CONFIG['DEVMAN_URL'], BOT_CONFIG['DEVMAN_TOKEN'], BOT_CONFIG['TIMEOUT']
    )

    logger.info('Devman API object has been initialized correctly.')

    telegram_bot = telegram.Bot(token=BOT_CONFIG['TELEGRAM_TOKEN'])

    logger.info('Telegram bot has been initialized correctly.')

    run_devman_long_polling(devman_api, telegram_bot, BOT_CONFIG['TELEGRAM_CHAT_ID'])


if __name__ == '__main__':
    main()
