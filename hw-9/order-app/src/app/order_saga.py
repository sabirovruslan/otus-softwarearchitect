import json

from app.auth_context import AuthContext
from app.models import Order
from app.producer import producer
from app.stories import OrderStoreStory


class OrderSaga:

    __TOPIC_RESERVE_ORDER = 'reserve_order'
    __TOPIC_PAY_ORDER = 'pay_order'

    def create_order(self, total_price, ctx: AuthContext, if_match: int):
        order = OrderStoreStory().execute(total_price, ctx, if_match)
        self._reserve_order(order)

        return order

    def _reserve_order(self, order: Order):
        producer.poll(0)
        producer.produce(
            self.__TOPIC_RESERVE_ORDER,
            json.dumps({'order_id': order.id}),
        )
        producer.flush()

    def pay_order(self, order: Order):
        producer.poll(0)
        producer.produce(
            self.__TOPIC_PAY_ORDER,
            json.dumps({'order_id': order.id, 'sum': order.total_price}),
        )
        producer.flush()
