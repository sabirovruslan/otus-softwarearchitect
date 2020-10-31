import json
from abc import abstractmethod, ABC
from typing import Dict

from app.auth_context import AuthContext
from app.exceptions import StoreValidation
from app.models import Order
from app.producer import producer
from app.repositories import OrderVersionRepository, OrderQueryRepository, OrderCommandRepository
from app.response_schema import get_orders_schema, order_store_schema


class StoreProtocol(ABC):

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplemented


class OrderStoreStory(StoreProtocol):
    __TOPIC = 'OrderCreated'

    def execute(self, total_price, ctx: AuthContext, if_match: int) -> dict:
        o_version = OrderVersionRepository.find_lock(ctx.id)
        if o_version.e_tag != if_match:
            raise StoreValidation(f"Order version {if_match} does not match")
        order = OrderCommandRepository.create(total_price, ctx.id, o_version)

        self.produce_event(order)

        return order_store_schema(order)

    def produce_event(self, order: Order):
        report = {}

        def delivery_report(err, msg):
            if err is not None:
                report.setdefault('err', err)
            else:
                report.setdefault('topic', msg.topic())
                report.setdefault('partition', msg.partition())

        producer.poll(0)
        producer.produce(
            self.__TOPIC,
            json.dumps({'order_id': order.id}),
            callback=delivery_report
        )
        producer.flush()


class GetOrdersStory(StoreProtocol):

    def execute(self, ctx: AuthContext) -> dict:
        o_version = OrderVersionRepository.find_or_create(ctx.id)
        orders = OrderQueryRepository.find_by(ctx.id)

        return get_orders_schema(orders, o_version)
