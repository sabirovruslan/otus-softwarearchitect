import os

from confluent_kafka.cimpl import Producer

producer = Producer({'bootstrap.servers': os.environ.get('BROKER')})

__all__ = 'producer'
