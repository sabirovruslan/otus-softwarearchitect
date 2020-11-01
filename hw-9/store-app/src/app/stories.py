import json
from abc import abstractmethod, ABC

from app.models import OrderStore
from app.producer import producer
from app.repositories import OrderStoreCommandRepository, OrderStoreQueryRepository
from app.response_schema import store_schema


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


class OrderStoreRejectStory(StoreProtocol):
    __TOPIC = 'order_reserve_rejected'

    def execute(self, order_id: int):
        store = OrderStoreQueryRepository.find_by(order_id)
        OrderStoreCommandRepository.update(store, OrderStore.Status.CANCELED)

        self.produce_event(store)

    def produce_event(self, store: OrderStore):
        producer.poll(0)
        producer.produce(
            self.__TOPIC,
            json.dumps({'order_id': store.order_id}),
        )
        producer.flush()


class GetOrderStoreStory(StoreProtocol):

    def execute(self, order_id: int):
        store = OrderStoreQueryRepository.find_by(order_id)

        return store_schema(store)
