from abc import abstractmethod, ABC

from app.auth_context import AuthContext
from app.repositories import OrderVersionRepository, OrderQueryRepository
from app.response_schema import get_orders_schema


class StoreProtocol(ABC):

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplemented


class OrderStoreStory(StoreProtocol):

    def execute(self, total_price: float, user_id: int) -> dict:
        return {}


class GetOrdersStory(StoreProtocol):

    def execute(self, ctx: AuthContext) -> dict:
        o_version = OrderVersionRepository.find_or_create(ctx.id)
        orders = OrderQueryRepository.find_by(ctx.id)

        return get_orders_schema(orders, o_version)
