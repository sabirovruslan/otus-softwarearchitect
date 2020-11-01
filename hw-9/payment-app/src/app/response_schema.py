from app.models import OrderPay


def health_schema() -> dict:
    return {'status': 'OK'}


def payment_schema(payment: OrderPay) -> dict:
    return {
        'id': payment.id,
        'order_id': payment.order_id,
        'status': payment.status,
    }
