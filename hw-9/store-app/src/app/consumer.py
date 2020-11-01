import json
import logging
import os

from confluent_kafka.cimpl import Consumer

from app.stories import OrderStoreStory, OrderStoreRejectStory


def reserve_order():
    consumer = Consumer({
        'bootstrap.servers': os.environ.get('BROKER'),
        'group.id': 'consumer-store-id',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['reserve_order'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error("Consumer error: {}".format(msg.error()))
            continue
        data = json.loads(msg.value())
        OrderStoreStory().execute(data.get('order_id'))

    consumer.close()


def reject_reserve_order():
    consumer = Consumer({
        'bootstrap.servers': os.environ.get('BROKER'),
        'group.id': 'consumer-store-reject-id',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['reject_reserve_order'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error("Consumer error: {}".format(msg.error()))
            continue
        data = json.loads(msg.value())
        OrderStoreRejectStory().execute(data.get('order_id'))

    consumer.close()


CONSUMERS = [reserve_order, reject_reserve_order]
