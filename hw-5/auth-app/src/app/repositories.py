from typing import Union

from app import db
from app.models import User


class UserQueryRepository:

    @staticmethod
    def find_by_phone(phone) -> User:
        return User.query.filter(User.phone == str(phone)).first()


class UserCommonRepository:

    @staticmethod
    def create(first_name: str, last_name: str, phone: Union[str, int]) -> User:
        user = User(phone=str(phone), first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        return user
