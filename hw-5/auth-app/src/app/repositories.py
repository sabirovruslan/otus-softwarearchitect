from typing import Union

from app import db
from app.models import User


class UserQueryRepository:

    @staticmethod
    def find_by_phone(phone: Union[str, int]) -> User:
        return User.query.filter(User.phone == str(phone)).first()


class UserCommonRepository:

    @staticmethod
    def create(first_name: str, last_name: str, phone: Union[str, int]) -> User:
        user = User(phone=str(phone), first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def update(user: User, first_name: str, last_name: str):
        user.first_name = first_name
        user.last_name = last_name
        db.session.commit()

    @staticmethod
    def confirmation(user: User, pin: str):
        user.pin = pin
        db.session.commit()

    @staticmethod
    def un_confirmation(user: User):
        user.pin = None
        db.session.commit()
