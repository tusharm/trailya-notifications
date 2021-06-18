import os
from typing import Optional

import firebase_admin

from datasets import factories
from utils.datetime import as_string
from utils.messaging import send_firebase_message
from storage.site import Site
from storage.sites_store import SitesStore
from utils.secrets import get_secret

firebase_admin.initialize_app()
store = SitesStore()


def notify(event, context):
    print(
        f'Triggered by messageId {context.event_id}, published at {context.timestamp} to {context.resource["name"]}')

    if 'attributes' not in event:
        print('No attributes found in the message, aborting..')
        return

    if 'state' not in event['attributes']:
        print('Attribute "state" not found in message, aborting..')
        return

    location = event['attributes']['state']

    if location not in factories:
        print(f'Unsupported location {location}')
        return

    process(location)


def process(location):
    api_key_id = os.getenv('VIC_API_KEY_ID')
    if api_key_id is None:
        print('Missing env var VIC_API_KEY_ID')
        return

    dataset = factories[location](get_secret(api_key_id))
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
    process('Victoria')
