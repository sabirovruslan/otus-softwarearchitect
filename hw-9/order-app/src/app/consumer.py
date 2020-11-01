import json
import logging
import os

from confluent_kafka.cimpl import Consumer

from app.order_saga import OrderSaga


def order_channel():
    consumer = Consumer({
        'bootstrap.servers': os.environ.get('BROKER'),
        'group.id': 'consumer-order-id',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['order_reserved', 'order_paid', 'order_pay_failed', 'order_reserve_rejected'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error("Consumer error: {}".format(msg.error()))
            continue
        msg.topic()
        data = json.loads(msg.value())
        topic = msg.topic()

        # TODO For demo
        if topic == 'order_reserved':
            OrderSaga().pay(data.get('order_id'))
            continue
        if topic == 'order_paid':
            OrderSaga().approve(data.get('order_id'))
            continue
        if topic == 'order_pay_failed':
            OrderSaga().reject_reserve(data.get('order_id'))
            continue
        if topic == 'order_reserve_rejected':
            OrderSaga().cancel(data.get('order_id'))
            continue

    consumer.close()


CONSUMERS = [order_channel]
