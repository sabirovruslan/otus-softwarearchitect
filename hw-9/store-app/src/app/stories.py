import json
from abc import abstractmethod, ABC

from app.models import OrderStore
from app.producer import producer
from app.repositories import OrderStoreCommandRepository


class StoreProtocol(ABC):

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplemented


class OrderStoreStory(StoreProtocol):
    __TOPIC = 'order_reserved'

    def execute(self, order_id: int):
        store = OrderStoreCommandRepository.create(order_id)

        self.produce_event(store)

    def produce_event(self, store: OrderStore):
        producer.poll(0)
        producer.produce(
            self.__TOPIC,
            json.dumps({'order_id': store.order_id}),
        )
        producer.flush()