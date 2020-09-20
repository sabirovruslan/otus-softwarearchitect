from app.models import User


def user_store_schema(user: User) -> dict:
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'is_active': user.is_active,
    }


def login_schema(token: str) -> dict:
    return {
        'token': token,
    }
