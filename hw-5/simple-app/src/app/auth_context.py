from functools import wraps
from typing import Optional

from flask import request


class AuthContext:
    phone: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    id: Optional[int]

    def __init__(self, **kwargs):
        self.id = kwargs.get('X-User-Id')
        self.first_name = kwargs.get('X-First-Name')
        self.last_name = kwargs.get('X-Last-Name')
        self.phone = kwargs.get('X-Phone')


def auth_context():
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            kwargs['ctx'] = AuthContext(**request.headers)

            return fn(*args, **kwargs)

        return decorated

    return wrapper
