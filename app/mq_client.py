from os import environ
from uuid import uuid4
from pathlib import Path
from json import loads, dumps


def initClient(channel):
    # Sending Requests
    TO_BE_PROCESSED = environ.get('MQ_TO_BE_PROCESSED_Q')
    request_uuid = str(uuid4())
    payload = {
        "request_id": request_uuid,
        "file_path": str(Path.joinpath(Path(__file__).parent.resolve(), 'tests',
                                       "resal.csv"))
    }
    channel.basic_publish(
        exchange='', routing_key=TO_BE_PROCESSED, body=dumps(payload))
    print(" [CLIENT] Sent Request: %r" % request_uuid)
    # Sending Requests End

    # Waiting for Responses
    PROCESSED = environ.get('MQ_PROCESSED_Q')

    def callback(ch, method, properties, body):
        request = loads(body)
        print(" [CLIENT] Received Processed Request %r" % request)

    channel.basic_consume(queue=PROCESSED,
                          on_message_callback=callback, auto_ack=True)

    print(' [CLIENT] Waiting for Processed Requests.')
    # Waiting for Responses End
