from datetime import datetime

from sqlalchemy import Column, DateTime, String, Boolean, Integer

from app import db


class DatetimeMixin:
    create_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_at = Column(DateTime, onupdate=datetime.utcnow)


class User(db.Model, DatetimeMixin):

    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(11), unique=True, nullable=False)
    pin = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)