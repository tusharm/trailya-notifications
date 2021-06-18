import backoff
import requests

from storage.site import Site


class RetryablException(Exception):
    pass


class VictoriaDataset:
    resource_id = 'afb52611-6061-4a2b-9110-74c920bede77'
    endpoint = 'https://wovg-community.gateway.prod.api.vic.gov.au/datavic/v1.2/datastore_search'
    page_size = 50

    def __init__(self, api_key: str):
        self.auth_header = {'apikey': api_key}

    @staticmethod
    def create(api_key: str):
        return VictoriaDataset(api_key)

    def sites(self) -> [Site]:
        params = {
            'resource_id': self.resource_id,
            'limit': self.page_size
        }

        sites = []
        for page in self._paged_get(params):
            sites = sites + [Site.from_dict(site) for site in page]

        return sites

    def _paged_get(self, params: dict):
        count = 0
        offset_param = {'offset': 0}
        while True:
            request_params = params.copy()
            request_params.update(offset_param)
            response = self._retryable_get(request_params)

            if not response.ok:
                raise Exception(
                    f'Unknown API error, code: {response.status_code}, text: {response.text}')

            response_data = response.json()
            if not response_data['success']:
                raise Exception(f'Error returned by dataset API call, message: {response_data["error"]["message"]}')

            records = response_data['result']['records']
            count += len(records)
            yield records

            print(f'Processed {count} records till now')
            if ('total' not in response_data['result']) or (count >= response_data['result']['total']):
                break

            offset_param['offset'] = count

    @backoff.on_exception(backoff.expo, RetryablException, max_time=120)
    def _retryable_get(self, params: dict):
        response = requests.request('GET', self.endpoint, headers=self.auth_header, params=params)
        if response.status_code == 429:
            raise RetryablException('Server is throttling, need to back off.')

        return response
