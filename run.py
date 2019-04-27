import os
import json

import requests
import telegram
from dotenv import load_dotenv

from logger_config import get_logger

logger = get_logger(__file__)


class DevmanApiAttribute:
    def __init__(self):
        self.val = None

    def __set__(self, instance, value):
        if instance.data is None:
            self.val = None
            return

        try:
            self.val = instance.data[value]
        except KeyError:
            self.val = None

    def __get__(self, instance, obj_type):
        return self.val


class DevmanApi:
    _timestamp = DevmanApiAttribute()
    _new_attempts = DevmanApiAttribute()

    def __init__(self, url, token, timeout):
        self.url = url
        self.token = token
        self.timeout = timeout
        self._data = None

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
        self._timestamp = 'timestamp_to_request'
        self._new_attempts = 'new_attempts'

    def _parse_response_body_to_dict(self, response):
        try:
            self._data = response.json()
        except json.JSONDecodeError:
            self._data = None

    @property
    def data(self):
        return self._data

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def new_attempts(self):
        return self._new_attempts


class TelegramNotification:
    def __init__(self, token, chat_id):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    def send_notification(self, text):
        self.bot.send_message(chat_id=self.chat_id, text=text)


def parse_attempt_data(attempt_data):
    lesson_title = attempt_data['lesson_title']
    title_response = f'Your task {lesson_title} has been examinated.'

    if attempt_data['is_negative']:
        body_response = 'Unfortunately, examinator had found some errors.'
    else:
        body_response = 'You can go ahead with a next task.'

    return '\n'.join([title_response, body_response])


def devman_long_polling(devman_api, telegram_notification_api):
    timestamp = None

    while True:

        try:

            devman_api.request(timestamp)

            timestamp = devman_api.timestamp
            new_attempts = devman_api.new_attempts

            logger.info(f'New timestamp has been recorded: {timestamp}.')

            if not new_attempts:
                logger.info('No new attempts were found.')
                continue

            for new_attempt in new_attempts:
                message_to_notificate = parse_attempt_data(new_attempt)
                telegram_notification_api.send_notification(message_to_notificate)

        except requests.Timeout as e:
            logger.error(e)
            continue
        except (requests.HTTPError, requests.RequestException) as e:
            logger.error(e)
            break


if __name__ == '__main__':
    load_dotenv()

    devman_url = 'https://dvmn.org/api/long_polling/'

    timeout = int(os.environ.get('TIMEOUT'))
    devman_api_token = os.environ.get('DEVMAN_TOKEN')
    telegram_bot_token = os.environ.get('TELEGRAM_TOKEN')
    telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    devman_api = DevmanApi(devman_url, devman_api_token, timeout)
    telegram_notification_api = TelegramNotification(telegram_bot_token, telegram_chat_id)

    devman_long_polling(devman_api, telegram_notification_api)
