from io import StringIO
from os import environ
from threading import Thread
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File
from app.services import product_service

# RestAPI
app = FastAPI()

@app.post("/product/top")
async def get_top_product(file: bytes = File(...)):
    csv_file = StringIO(file.decode("utf-8"))
    res = product_service.process_top_product(csv_file)

    return res

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from app.mq_client import initClient
from app.mq_server import initServer

# Setup message broker
def start_consumer():
    credentials = PlainCredentials(environ.get('MQ_USER'), environ.get('MQ_PASS'))
    parameters = ConnectionParameters(environ.get("MQ_URL"),
                                        environ.get('MQ_PORT'),
                                        '/',
                                        credentials)
    connection = BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=environ.get('MQ_TO_BE_PROCESSED_Q'))
    channel.queue_declare(queue=environ.get('MQ_PROCESSED_Q'))

    # Message Based
    initServer(channel)
    initClient(channel)
    channel.start_consuming()

consumer_thread = Thread(target=start_consumer, daemon=True)
consumer_thread.start()