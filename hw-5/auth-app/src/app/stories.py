from abc import abstractmethod, ABC

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
