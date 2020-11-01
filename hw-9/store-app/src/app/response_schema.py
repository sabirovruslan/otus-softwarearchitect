from app.models import OrderStore


def health_schema() -> dict:
    return {'status': 'OK'}


def store_schema(store: OrderStore) -> dict:
    return {
        'id': store.id,
        'order_id': store.order_id,
        'status': store.status,
    }
