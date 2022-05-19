import pika
import json
import os
from dotenv import load_dotenv
load_dotenv('.env')

MQ_HOST = os.getenv('MQ_HOST')
MQ_PORT = os.getenv('MQ_PORT')
MQ_USER = os.getenv('MQ_USER')
MQ_PASSWD = os.getenv('MQ_PASSWD')

# params = pika.URLParameters(MQ_HOST)

# params = pika.ConnectionParameters(host='rabbitmq', credentials=pika.credentials.PlainCredentials(
#     MQ_USER, MQ_PASSWD), heartbeat=10)
# params = pika.ConnectionParameters("localhost", heartbeat=10)

# params = pika.URLParameters('amqp://guest:guest@rabbitmq:5672')
params = pika.URLParameters(
    'amqp://myuser:mypassword@rabbitmq:5672?heartbeat=0&blocked_connection_timeout=0')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body, service='player'):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key=service, body=json.dumps(body), properties=properties)
    # print(" [x] Sent %r" % body)
