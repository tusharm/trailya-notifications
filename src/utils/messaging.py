from firebase_admin import messaging


def send_firebase_message(location_state: str, sites_count: int):
    message = messaging.Message(
        topic=f'/topics/{location_state}',
        notification=messaging.Notification(
            title='Exposure sites update',
            body=f'{location_state} has recorded {sites_count} new exposure sites.'
        ),
        data={
            'type': 'site'
        },
        android=messaging.AndroidConfig(priority='normal', ttl=3600)
    )
    response = messaging.send(message)
    # Response is a message ID string.
    print(f'Successfully sent message: {response}')
