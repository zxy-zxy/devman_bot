import requests
import json


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
