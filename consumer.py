from confluent_kafka import Consumer, KafkaError
import pymongo
import json
import signal
import sys

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
})

topics = ['exchangerate', 'openweathermap']
consumer.subscribe(topics)

client = pymongo.MongoClient('mongodb+srv://dbUser:010801Haziel@cluster0.dx95efh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['CPD']

topic_to_collection = {
    'exchangerate': db['exchangerate'],
    'openweathermap': db['openweathermap']
}

def signal_handler(sig, frame):
    print('Deteniendo el script...')
    consumer.close()
    client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        print(f"Mensaje recibido de {msg.topic()} - Offset: {msg.offset()}")

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
    client.close()