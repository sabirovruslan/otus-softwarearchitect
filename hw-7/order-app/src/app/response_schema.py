from typing import List

from app.models import Order, OrderVersion


def get_orders_schema(orders: List[Order], version: OrderVersion) -> dict:
    return {
        'e_tag': version.e_tag,
        'orders': [
            {
                'id': order.id,
                'total_price': order.total_price,
            }
            for order in orders
        ]
    }


def order_store_schema(order: Order) -> dict:
    return {
        'id': order.id,
        'total_price': order.total_price,
    }


def health_schema() -> dict:
    return {'status': 'OK'}
