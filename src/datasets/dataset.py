import backoff
import requests


class RetryableException(Exception):
    pass


class Dataset:
    @backoff.on_exception(backoff.expo, RetryableException, max_time=120)
    def get_with_retries(self, endpoint, headers: dict = {}, params: dict = {}):
        response = requests.request('GET', endpoint, headers=headers, params=params)
        if response.status_code == 429:
            raise RetryableException('Server is throttling, need to back off.')

        if not response.ok:
            raise Exception(
                f'Unknown API error, code: {response.status_code}, text: {response.text}')

        return response
