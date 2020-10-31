import json
import logging
import os

from confluent_kafka.cimpl import Consumer

from app.stories import OrderPayStory


def pay_order():
    consumer = Consumer({
        'bootstrap.servers': os.environ.get('BROKER'),
        'group.id': 'consumer-pay-id',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['pay_order'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error("Consumer error: {}".format(msg.error()))
            continue
        data = json.loads(msg.value())
        OrderPayStory().execute(data.get('order_id'))

    consumer.close()


CONSUMERS = [pay_order]
