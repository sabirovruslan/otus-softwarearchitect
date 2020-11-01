import json
import random
from abc import abstractmethod, ABC

from app.models import OrderPay
from app.producer import producer
from app.repositories import OrderPayCommandRepository


class StoreProtocol(ABC):

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplemented


class OrderPayStory(StoreProtocol):
    __TOPIC = 'order_paid'
    __TOPIC_ERROR = 'order_pay_failed'

    def execute(self, order_id: int):
        if random.random() > .7:
            self.produce_error_event(order_id)
        else:
            payment = OrderPayCommandRepository.create(order_id)
            self.produce_event(payment)

    def produce_event(self, payment: OrderPay):
        producer.poll(0)
        producer.produce(
            self.__TOPIC,
            json.dumps({'order_id': payment.order_id}),
        )
        producer.flush()

    def produce_error_event(self, order_id):
        producer.poll(0)
        producer.produce(
            self.__TOPIC_ERROR,
            json.dumps({'order_id': order_id}),
        )
        producer.flush()
