from sqlalchemy import Column, BigInteger, Numeric, Integer, String

from app.db import db


class Order(db.Model):
    __tablename__ = "orders"

    class Status:
        RESERVE_PENDING = 'reserve_pending'
        REJECT_RESERVE_PENDING = 'reject_reserve_pending'
        PAY_PENDING = 'pay_pending'
        APPROVE_PENDING = 'approve_pending'
        APPROVED = 'approved'
        CANCELED = 'canceled'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    total_price = Column(Numeric(6, 2), nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(BigInteger, nullable=False)


class OrderVersion(db.Model):
    __tablename__ = "orders_version"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, nullable=False, unique=True)
    e_tag = Column(Integer, nullable=False, default=0)
