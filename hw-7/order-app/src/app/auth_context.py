from functools import wraps
from typing import Optional

from flask import request


class AuthContext:
    id: Optional[int]

    def __init__(self, **kwargs):
        self.id = kwargs.get('X-User-Id')


def auth_context():
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            kwargs['ctx'] = AuthContext(**request.headers)

            return fn(*args, **kwargs)

        return decorated

    return wrapper
