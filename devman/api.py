import requests


class DevmanApi:

    default_timeout = 100

    def __init__(self, url, token, timeout=None):
        self.url = url
        self.token = token
        self.timeout = timeout or DevmanApi.default_timeout

    def request(self, timestamp=None):
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.get(
            self.url,
            headers=headers,
            timeout=self.timeout,
            params={'timestamp': timestamp}
        )
        response.raise_for_status()
        return response
