import re
from datetime import datetime

from datasets.dataset import Dataset
from datasets.errors import DatasetErrors
from storage.site import Site
from utils.dateutils import parse_to_utc


class NSWDataset(Dataset):
    """
    Returns NSW exposure sites.
    """

    endpoint = 'https://data.nsw.gov.au/data/' \
               'dataset/0a52e6c1-bc0b-48af-8b45-d791a6d8e289/' \
               'resource/f3a28eed-8c2a-437b-8ac1-2dab3cf760f9/' \
               'download/covid-case-locations'

    def __init__(self):
        self.parser = NSWSiteParser()

    def sites(self) -> [Site]:
        response = self.get_with_retries(self.endpoint)

        sites = list(map(lambda s: self.parser.to_site(s), response.json()['data']['monitor']))
        print(f"Got {len(response.json()['data']['monitor'])} site results")
        return sites


class NSWSiteParser:
    timezone = 'Australia/Sydney'
    time_pattern = re.compile(r'(\d?\d?[:.]?\d?\d[ap]m)')
    latlng_pattern = re.compile(r'([-]?\d+\.\d+)')

    def to_site(self, site: dict) -> Site:
        errors = DatasetErrors()

        added_time = parse_to_utc(f'{site["Last updated date"]}T00:00:00', self.timezone)
        exposure_start_time, exposure_end_time = self._get_exposure_times(site, errors, added_time)

        lat, long = self._get_lat_long(site, errors)

        return Site(
            suburb=site['Suburb'],
            title=site['Venue'],
            street_address=site['Address'],
            state='NSW',
            postcode=None,
            exposure_start_time=exposure_start_time,
            exposure_end_time=exposure_end_time,
            added_time=added_time,
            latitude=lat,
            longitude=long,
            geocode={},
            data_errors=errors.get(),
        )

    def _get_lat_long(self, site: dict, errors: DatasetErrors):
        lat = errors.try_operation(lambda: float(site['Lat']), None, msg=f'Error parsing \'Lat\' field: {site["Lat"]}')
        long = errors.try_operation(lambda: float(site['Lon']), None, msg=f'Error parsing \'Lon\' field: {site["Lon"]}')
        return lat, long

    def _get_exposure_times(self, site: dict, errors: DatasetErrors, default: datetime):
        error_msg = f'Error parsing \'Time\' field value: {site["Time"]}'
        exposure_times = self.time_pattern.findall(site['Time'])

        start_time = errors.try_operation(lambda: exposure_times[0], '12:00am', msg=error_msg).replace('.', ':')
        exposure_start_time = errors.try_operation(
            lambda: parse_to_utc(f'{site["Date"]} {start_time}', self.timezone),
            default,
            f'Error parsing \'Date\' field value in \'{site["Date"]} {start_time}\''
        )

        end_time = errors.try_operation(lambda: exposure_times[1], '11:59pm', msg=error_msg).replace('.', ':')
        exposure_end_time = errors.try_operation(
            lambda: parse_to_utc(f'{site["Date"]} {end_time}', self.timezone),
            default,
            f'Error parsing \'Date\' field value in \'{site["Date"]} {end_time}\''
        )

        return exposure_start_time, exposure_end_time


if __name__ == '__main__':
    dataset = NSWDataset()
    sites = dataset.sites()
    for s in sites:
        print(s)

    print(f'Total no of sites: {len(sites)}')

