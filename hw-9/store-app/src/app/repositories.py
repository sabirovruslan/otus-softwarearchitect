from typing import Union

from app.db import db
from app.models import OrderStore


class OrderStoreQueryRepository:

    @staticmethod
    def find_by(order_id: Union[str, int]) -> OrderStore:
        return OrderStore.query.filter(OrderStore.order_id == int(order_id)).first()


class OrderStoreCommandRepository:

    @staticmethod
    def create(order_id: Union[str, int]) -> OrderStore:
        store = OrderStore(order_id=int(order_id), status=OrderStore.Status.COMPLETED)
        db.session.add(store)
        db.session.commit()

        return store

    @staticmethod
    def update(store: OrderStore, status: str):
        store.status = status
        db.session.commit()
