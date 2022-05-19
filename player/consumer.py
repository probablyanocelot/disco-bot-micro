import pika
import os
import json
from app import db, Song
from dotenv import load_dotenv
load_dotenv('.env')

MQ_HOST = os.getenv('MQ_HOST')
MQ_PORT = os.getenv('MQ_PORT')
MQ_USER = os.getenv('MQ_USER')
MQ_PASSWD = os.getenv('MQ_PASSWD')

# params = pika.URLParameters(MQ_HOST)

# params = pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, credentials=pika.credentials.PlainCredentials(
#     MQ_USER, MQ_PASSWD), heartbeat=10)

params = pika.URLParameters(
    'amqp://myuser:mypassword@rabbitmq:5672?heartbeat=0&blocked_connection_timeout=0')


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='player')


def callback(ch, method, properties, body):
    print('Received in Player')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'song_created':
        song = Song(title=data['title'], url=data['url'])
        db.session.add(song)
        db.session.commit()
        print('Song Added')
        # requests.get(
        #     'http://backend:5000/api/query/song_added/{}'.format(song.id))

    elif properties.content_type == 'song_updated':
        song = Song.query.get(data['id'])
        song.title = data['title']
        song.image = data['url']
        db.session.commit()
        print('Song Updated')

    elif properties.content_type == 'song_deleted':
        song = Song.query.get(data)
        db.session.delete(song)
        db.session.commit()
        print('Song Deleted')


channel.basic_consume(queue='player',
                      on_message_callback=callback)  # auto_ack=True

print('Started Consuming')

channel.start_consuming()

channel.close()
