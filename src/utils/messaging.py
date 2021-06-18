from firebase_admin import messaging


def send_firebase_message(location_state: str, sites_count: int):
    message = messaging.Message(
        topic=f'/topics/{location_state}',
        notification=messaging.Notification(
            title=f'{sites_count} new exposure sites for {location_state}'
        )
    )
    response = messaging.send(message)
    # Response is a message ID string.
    print(f'Successfully sent message: {response}')
