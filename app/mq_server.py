
from os import environ

def initServer(channel):
    TO_BE_PROCESSED = environ.get('MQ_TO_BE_PROCESSED_Q')
    
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=TO_BE_PROCESSED, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
