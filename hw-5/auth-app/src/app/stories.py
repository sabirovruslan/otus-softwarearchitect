from abc import abstractmethod, ABC
from typing import Union

from flask_security.utils import hash_password

from app.exceptions import StoreValidation
from app.repositories import UserQueryRepository, UserCommonRepository
from app.response_schema import user_store_schema


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
