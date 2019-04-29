import os
import json

import requests
import telegram
from dotenv import load_dotenv

from logger_config import get_logger

logger = get_logger(__file__)


class DevmanApi:

    def __init__(self, url, token, timeout):
        self.url = url
        self.token = token
        self.timeout = timeout

    def request(self, timestamp=None):
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.get(
            self.url,
            headers=headers,
            timeout=self.timeout,
            params={'timestamp': timestamp}
        )
        response.raise_for_status()
        self._parse_response_body_to_dict(response)
        data = DevmanApi._parse_response_body_to_dict(response)
        return data

    @staticmethod
    def _parse_response_body_to_dict(response):
        try:
            return response.json()
        except json.JSONDecodeError:
            return None


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
    load_dotenv()

    devman_url = 'https://dvmn.org/api/long_polling/'

    timeout = int(os.environ.get('TIMEOUT'))
    devman_api_token = os.environ.get('DEVMAN_TOKEN')
    telegram_bot_token = os.environ.get('TELEGRAM_TOKEN')
    telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    devman_api = DevmanApi(devman_url, devman_api_token, timeout)

    telegram_bot = telegram.Bot(token=telegram_bot_token)

    run_devman_long_polling(devman_api, telegram_bot, telegram_chat_id)


if __name__ == '__main__':
    main()
