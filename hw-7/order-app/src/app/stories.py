from abc import abstractmethod, ABC
from time import sleep

from app.auth_context import AuthContext
from app.exceptions import StoreValidation
from app.repositories import OrderVersionRepository, OrderQueryRepository, OrderCommandRepository
from app.response_schema import get_orders_schema, order_store_schema


class StoreProtocol(ABC):

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplemented


class OrderStoreStory(StoreProtocol):

    def execute(self, total_price, ctx: AuthContext, if_match: int) -> dict:
        o_version = OrderVersionRepository.find_lock(ctx.id)
        if o_version.e_tag != if_match:
            raise StoreValidation(f"Order version {if_match} does not match")
        return order_store_schema(OrderCommandRepository.create(total_price, ctx.id, o_version))


class GetOrdersStory(StoreProtocol):

    def execute(self, ctx: AuthContext) -> dict:
        o_version = OrderVersionRepository.find_or_create(ctx.id)
        orders = OrderQueryRepository.find_by(ctx.id)

        return get_orders_schema(orders, o_version)
