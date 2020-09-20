from flask import current_app

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


def health_schema() -> dict:
    return {'status': 'OK'}


def jwks_schema() -> dict:
    from authlib.jose import JsonWebKey
    from authlib.jose import JWK_ALGORITHMS

    jwk = JsonWebKey(algorithms=JWK_ALGORITHMS)
    key = jwk.dumps(current_app.config['PUBLIC_KEY'], kty='RSA')
    key['kid'] = '1'

    return {'keys': [key]}
