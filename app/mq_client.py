from os import environ

def initClient(channel):
    TO_BE_PROCESSED = environ.get('MQ_TO_BE_PROCESSED_Q')
    channel.basic_publish(exchange='', routing_key=TO_BE_PROCESSED, body='Hello World!')
    print(" [x] Sent 'Hello World!'")