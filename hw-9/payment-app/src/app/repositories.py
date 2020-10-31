from typing import Union

from app.db import db
from app.models import OrderPay


class OrderPayQueryRepository:

    @staticmethod
    def find_by(order_id: Union[str, int]) -> OrderPay:
        return OrderPay.query.filter(OrderPay.order_id == int(order_id)).first()


class OrderPayCommandRepository:

    @staticmethod
    def create(order_id: Union[str, int]) -> OrderPay:
        pay = OrderPay(order_id=int(order_id), status=OrderPay.Status.COMPLETED)
        db.session.add(pay)
        db.session.commit()

        return pay
