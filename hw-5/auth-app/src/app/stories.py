from abc import abstractmethod, ABC
from datetime import datetime, timedelta
from typing import Union

import jwt
from flask import current_app
from flask_security.utils import hash_password, verify_password

from app.auth_context import AuthContext
from app.exceptions import StoreValidation
from app.models import User
from app.repositories import UserQueryRepository, UserCommonRepository
from app.response_schema import user_store_schema, login_schema


class StoreProtocol(ABC):

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplemented


class UserStoreStory(StoreProtocol):

    def execute(self, first_name: str, last_name: str, phone: int) -> dict:
        user = UserQueryRepository.find_by_phone(phone)
        if user is not None:
            raise StoreValidation('User already exists')

        try:
            user = UserCommonRepository.create(first_name=first_name, last_name=last_name, phone=phone)
        except Exception:
            raise StoreValidation('Failed to create user')

        return user_store_schema(user)


class UserUpdateByCtxStory(StoreProtocol):

    def execute(self, ctx: AuthContext, first_name: str, last_name: str):
        user = UserQueryRepository.find_by_phone(ctx.phone)
        if user is None:
            raise StoreValidation(f"User not exists by phone:{ctx.phone} ctx:{ctx}")

        try:
            UserCommonRepository.update(user, first_name=first_name, last_name=last_name)
        except Exception:
            raise StoreValidation('Failed to update user')


class GetConfirmationStory(StoreProtocol):

    @staticmethod
    def __generate_pin():
        # TODO for demo auth
        return 12345

    def execute(self, phone: Union[str, int]):
        user = UserQueryRepository.find_by_phone(phone)
        if user is None:
            raise StoreValidation('User not exists')

        pin = self.__generate_pin()
        UserCommonRepository.confirmation(user, hash_password(str(pin)))

        # TODO sent event=CREATE_CONFIRMATION to broker


class UserLoginStory(StoreProtocol):

    def execute(self, phone: Union[str, int], pin: int) -> dict:
        user = UserQueryRepository.find_by_phone(phone)
        if user is None:
            raise StoreValidation('User not exists')

        self.__validate_pin(user.pin, pin)
        token = self.__create_id_token(user)
        UserCommonRepository.un_confirmation(user)

        return login_schema(token)

    @staticmethod
    def __validate_pin(pin_hash, pin):
        if pin_hash is None or len(pin_hash) == 0 or not verify_password(str(pin), pin_hash):
            raise StoreValidation('Invalid confirmation code')

    @staticmethod
    def __create_id_token(user: User) -> str:
        data = {
            "iss": "http://arch.homework",
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "sub": user.id,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        encoded = jwt.encode(data, current_app.config['PRIVATE_KEY'], algorithm='RS256', headers={'kid': '1'})

        return encoded.decode('utf-8')


class AuthStory(StoreProtocol):

    def execute(self, token: str) -> dict:
        encoded = jwt.decode(token, current_app.config['PUBLIC_KEY'], algorithms=['RS256'])
        headers = {
            'X-User-Id': encoded.get('sub'),
            'X-First-Name': encoded.get('first_name'),
            'X-Last-Name': encoded.get('last_name'),
            'X-Phone': encoded.get('phone'),
        }

        return headers
