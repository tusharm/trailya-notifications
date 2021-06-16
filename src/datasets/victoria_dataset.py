import json

import requests

from storage.site import Site


class VictoriaDataset:
    resource_id = 'afb52611-6061-4a2b-9110-74c920bede77'
    endpoint = 'https://discover.data.vic.gov.au/api/3/action/datastore_search'

    def __init__(self, api_key: str):
        self.auth_header = {'Authorization': api_key}

    @staticmethod
    def create(api_key: str):
        return VictoriaDataset(api_key)

    def sites(self) -> [Site]:
        params = {
            'resource_id': self.resource_id,
            'limit': 5
        }
        response = requests.get(self.endpoint, params=params, headers=self.auth_header)
        if not response.ok:
            print(f'Got error response from data API: {response.status_code}')
            return None

        data = response.json()
        if not data['success']:
            print(f'Unsuccessful response from data API, response content: {data}')
            return None

        return [Site.from_dict(e) for e in data['result']['records']]

