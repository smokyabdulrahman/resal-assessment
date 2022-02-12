from io import StringIO
from os import environ
from json import loads, dumps
from app.services import product_service

def initServer(channel):
    TO_BE_PROCESSED = environ.get('MQ_TO_BE_PROCESSED_Q')
    PROCESSED = environ.get('MQ_PROCESSED_Q')
    print(' [SERVER] Hmm...')
    def callback(ch, method, properties, body):
        request = loads(body)
        print(" [SERVER] Received %r" % request)
        f = open(request["file_path"], "rb")
        response = dumps(product_service.process_top_product(
            StringIO(f.read().decode("utf-8"))), default=lambda o: o.__dict__,
                                          sort_keys=True, indent=4)
        print(" [SERVER] Done %r" % response)

        payload = {
            "request_id": request["request_id"],
            "response": response
        }

        channel.basic_publish(
            exchange='', routing_key=PROCESSED, body=dumps(payload))
        print(" [SERVER] Pushed response back.")

    channel.basic_consume(queue=TO_BE_PROCESSED,
                          on_message_callback=callback, auto_ack=True)

    print(' [SERVER] Waiting for requests.')
