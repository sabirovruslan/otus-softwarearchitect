from typing import List

from app.models import Order, OrderVersion


def get_orders_schema(orders: List[Order], version: OrderVersion) -> dict:
    return {
        'e_tag': version.e_tag,
        'orders': [
            order_store_schema(order)
            for order in orders
        ]
    }


def order_store_schema(order: Order) -> dict:
    return {
        'id': order.id,
        'status': order.status,
        'total_price': float(order.total_price),
    }


def health_schema() -> dict:
    return {'status': 'OK'}
