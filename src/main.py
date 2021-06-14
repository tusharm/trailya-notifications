import firebase_admin
from firebase_admin import messaging


def notify(event, context):
    print(f"""Triggered by messageId {context.event_id}, published at {context.timestamp} to {context.resource["name"]}""")

    if 'attributes' not in event:
        print('No attributes found in the message, aborting..')
        return

    if 'state' not in event['attributes']:
        print('Attribute "state" not found in message, aborting..')
        return

    firebase_admin.initialize_app()
    location_state = event['attributes']['state']

    # See documentation on defining a message payload.
    message = messaging.Message(
        topic=f'/topics/{location_state}',
        notification=messaging.Notification(
            title=f'New exposure site for {location_state}'
        )
    )

    response = messaging.send(message)

    # Response is a message ID string.
    print(f'Successfully sent message: {response}')
