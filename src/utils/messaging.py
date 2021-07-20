import logging

from firebase_admin import messaging

log = logging.getLogger(__name__)


def send_firebase_message(location_state: str, sites_count: int):
    message = messaging.Message(
        topic=f'/topics/{location_state}',
        notification=messaging.Notification(
            title='Exposure sites update',
            body=f'{location_state} has recorded {sites_count} new exposure sites.'
        ),
        data={
            'type': 'sites_update'
        },
        android=messaging.AndroidConfig(priority='normal', ttl=86400)
    )
    response = messaging.send(message)
    # Response is a message ID string.
    log.info(f'Successfully published sites update message: {response}')
