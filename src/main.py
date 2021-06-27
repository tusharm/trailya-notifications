from typing import Optional

import firebase_admin

from config import config_factory
from storage.site import Site
from storage.sites_store import SitesStore
from utils.dateutils import as_string
from utils.geocoder import Geocoder
from utils.messaging import send_firebase_message

firebase_admin.initialize_app()


def notify(event, context):
    print(
        f'Triggered by messageId {context.event_id}, published at {context.timestamp} to {context.resource["name"]}')

    if 'attributes' not in event:
        raise Exception('No attributes found in the message, aborting..')

    if 'state' not in event['attributes']:
        raise Exception('Attribute "state" not found in message, aborting..')

    location = event['attributes']['state']
    process(location)


def process(location: str):
    config = config_factory(location)
    if config is None:
        raise Exception(f'Unknown location: {location}')

    dataset = config.dataset_service()

    store = SitesStore(Geocoder(config.maps_api_key()), location=location)
    last_updated_on = store.last_updated_on()

    updated_sites = new_sites_since(last_updated_on, dataset)
    if len(updated_sites) == 0:
        print(f'No new exposure sites found since last run ({last_updated_on})')
        return

    print(f'Found {len(updated_sites)} new exposure sites since last run on {last_updated_on}')
    store.save(updated_sites)

    send_firebase_message(location, len(updated_sites))


def new_sites_since(last_update_date: Optional[str], dataset) -> [Site]:
    sites = dataset.sites()

    if last_update_date is None:
        return sites

    sorted_sites = sorted(sites, key=lambda s: s.added_time, reverse=True)

    for idx, site in enumerate(sorted_sites):
        if as_string(site.added_time) == last_update_date:
            return sorted_sites[0:idx]

    return []


if __name__ == '__main__':
    process('NSW')
