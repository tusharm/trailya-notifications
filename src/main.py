import os
from typing import Optional

import firebase_admin

from datasets import factories
from dateutils import as_string
from storage.site import Site
from storage.sites_store import SitesStore

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
    api_key = os.getenv('API_KEY')
    if api_key is None:
        print('Missing env var API_KEY')
        return

    dataset = factories[location](api_key)
    last_updated_on = store.last_updated_on()

    updated_sites = new_sites_since(last_updated_on, dataset)

    print(f'Found {len(updated_sites)} updated sites since last run on {last_updated_on}')
    store.save(updated_sites)

    # send_firebase_message(location)


def new_sites_since(last_update_date: Optional[str], dataset) -> [Site]:
    sites = dataset.sites()
    if last_update_date is None:
        return sites

    sorted_sites = sorted(dataset.sites(), key=lambda s: s.added_time, reverse=True)

    for idx, site in enumerate(sorted_sites):
        if as_string(site.added_time) == last_update_date:
            return sorted_sites[0:idx]

    return []


if __name__ == '__main__':
    process('Victoria')
