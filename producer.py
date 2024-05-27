import signal
import sys
from confluent_kafka import Producer
import requests
import json
import time

producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(producer_config)

apis = {
    'exchangerate': {
        'url': 'https://v6.exchangerate-api.com/v6/78a0c87d8bdf7de31ab7d577/latest/USD',
        'params': {}
    },
    'openweathermap': {
        'url': 'https://api.openweathermap.org/data/2.5/weather',
        'params': {
            'lat': '28.5',
            'lon': '-106',
            'appid': '836da4723c94834195be9859fac8d018'
        }
    }
}

def fetch_data(api):
    params = api.get('params', {})
    response = requests.get(api['url'], params=params)
    if response.status_code == 200:
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(f'Error: No se pudo decodificar la respuesta JSON de {api["url"]}')
            return None
    else:
        print(f'Error fetching data from {api["url"]}: {response.status_code}')
        return None

def produce_message(topic, data):
    producer.produce(topic, json.dumps(data).encode('utf-8'))
    producer.flush()

def signal_handler(sig, frame):
    print('Deteniendo el script...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    for topic, api in apis.items():
        data = fetch_data(api)
        if data:
            produce_message(topic, data)
            print(f'Produced message to {topic}')
        else:
            print(f'Failed to fetch data for {topic}')

    time.sleep(300)
