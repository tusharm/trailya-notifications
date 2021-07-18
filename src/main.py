import firebase_admin
import logging

from config import config_factory
from storage.sites_store import SitesStore
from utils.geocoder import Geocoder
from utils.messaging import send_firebase_message

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s (%(name)s)', level=logging.INFO)
log = logging.getLogger(__name__)

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


def process(location: str, debug=False):
    config = config_factory(location)
    if config is None:
        raise Exception(f'Unknown location: {location}')

    dataset = config.dataset_service()

    store = SitesStore(Geocoder(config.maps_api_key()), location=location)
    updated_count = store.update(dataset.sites())
    log.info(f'No of sites updated for {location}: {updated_count}')

    if not debug and updated_count != 0:
        send_firebase_message(location, updated_count)


if __name__ == '__main__':
    process('NSW', debug=True)
