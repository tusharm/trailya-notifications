def notify(event, context):
    print(f'Triggered by messageId {context.event_id}, published at {context.timestamp} to {context.resource["name"]}')
    
    if 'attributes' not in event:
        print('No attributes found in the message, aborting..')
        return

    print(f'Got a message with attribute {event["attributes"]}')

    
