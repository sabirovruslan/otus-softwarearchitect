import json
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

    def execute(self, order_id: int):
        store = OrderPayCommandRepository.create(order_id)

        self.produce_event(store)

    def produce_event(self, store: OrderPay):
        producer.poll(0)
        producer.produce(
            self.__TOPIC,
            json.dumps({'order_id': store.order_id}),
        )
        producer.flush()