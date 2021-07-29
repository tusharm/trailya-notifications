import logging

from datasets.dataset import Dataset
from storage.site import Site
from utils.dateutils import parse_to_utc

log = logging.getLogger(__name__)


class VictoriaDataset(Dataset):
    resource_id = 'afb52611-6061-4a2b-9110-74c920bede77'
    endpoint = 'https://wovg-community.gateway.prod.api.vic.gov.au/datavic/v1.2/datastore_search'
    page_size = 50

    def __init__(self, api_key: str):
        self.auth_header = {'apikey': api_key}
        self.parser = VictoriaSiteParser()

    @staticmethod
    def create(api_key: str):
        return VictoriaDataset(api_key)

    def sites(self) -> [Site]:
        params = {
            'resource_id': self.resource_id,
            'limit': self.page_size
        }

        site_list = []
        for page in self._paged_get(params):
            site_list = site_list + [self.parser.to_site(site) for site in page]

        log.info(f'Got {len(site_list)} sites from VIC dataset API.')
        return site_list

    def _paged_get(self, params: dict):
        count = 0
        offset_param = {'offset': 0}
        while True:
            request_params = params.copy()
            request_params.update(offset_param)
            response = self.get_with_retries(self.endpoint, params=request_params, headers=self.auth_header)

            response_data = response.json()
            if not response_data['success']:
                raise Exception(f'Error returned by dataset API call, message: {response_data["error"]["message"]}')

            records = response_data['result']['records']
            count += len(records)
            yield records

            if ('total' not in response_data['result']) or (count >= response_data['result']['total']):
                break

            offset_param['offset'] = count


class VictoriaSiteParser:
    timezone = 'Australia/Melbourne'

    def to_site(self, site: dict) -> Site:
        exposure_start_time = parse_to_utc(f"{site['Exposure_date_dtm']} {site['Exposure_time_start_24']}",
                                           self.timezone)
        exposure_end_time = parse_to_utc(f"{site['Exposure_date_dtm']} {site['Exposure_time_end_24']}", self.timezone)
        added_time = parse_to_utc(f"{site['Added_date_dtm']} {site['Added_time']}", self.timezone)

        return Site(
            site['Suburb'],
            site['Site_title'],
            site['Site_streetaddress'],
            site['Site_state'],
            int(site['Site_postcode']) if site['Site_postcode'] else None,
            exposure_start_time,
            exposure_end_time,
            added_time,
            None,
            None,
            {},
            {}
        )


if __name__ == '__main__':
    import os

    if 'VIC_API_KEY' not in os.environ:
        raise Exception('Missing env var VIC_API_KEY')

    dataset = VictoriaDataset(os.environ['VIC_API_KEY'])
    sites = dataset.sites()
    for s in sites:
        print(s)

    print(f'Total no of sites: {len(sites)}')
