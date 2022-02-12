from os import environ
from dotenv import load_dotenv
load_dotenv()

from multiprocessing import connection
from fastapi import FastAPI
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from app.mq_client import initClient
from app.mq_server import initServer

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
initClient(channel)
initServer(channel)

# RestAPI
app = FastAPI()