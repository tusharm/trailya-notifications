import firebase_admin
from firebase_admin import messaging


def send_firebase_message(location_state: str):
    firebase_admin.initialize_app()

    message = messaging.Message(
        topic=f'/topics/{location_state}',
        notification=messaging.Notification(
            title=f'New exposure site for {location_state}'
        )
    )
    response = messaging.send(message)
    # Response is a message ID string.
    print(f'Successfully sent message: {response}')
