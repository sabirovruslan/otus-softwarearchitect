from sqlalchemy import Column, BigInteger, Numeric, Integer

from app import db


class Order(db.Model):
    __tablename__ = "orders"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    total_price = Column(Numeric(6, 2), nullable=False)
    user_id = Column(BigInteger, nullable=False)


class OrderVersion(db.Model):
    __tablename__ = "orders_version"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, nullable=False, unique=True)
    e_tag = Column(Integer, nullable=False, default=0)
