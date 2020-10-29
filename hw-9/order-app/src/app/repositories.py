from typing import List, Union

from app import db
from app.models import OrderVersion, Order


class OrderVersionRepository:

    @staticmethod
    def find_or_create(user_id: Union[str, int]) -> OrderVersion:
        version = OrderVersion.query.filter(OrderVersion.user_id == int(user_id)).first()
        if not version:
            version = OrderVersion(user_id=user_id)
            db.session.add(version)
            db.session.commit()

        return version

    @staticmethod
    def find_lock(user_id: Union[str, int]) -> OrderVersion:
        version = OrderVersion.query.filter(OrderVersion.user_id == int(user_id)).with_for_update().first()

        return version


class OrderQueryRepository:

    @staticmethod
    def find_by(user_id: Union[str, int]) -> List[Order]:
        return Order.query.filter(Order.user_id == int(user_id)).all()


class OrderCommandRepository:

    @staticmethod
    def create(total_price, user_id: Union[str, int], version: OrderVersion) -> Order:
        order = Order(total_price=total_price, user_id=user_id)
        version.e_tag += 1
        db.session.add(order)
        db.session.commit()

        return order
