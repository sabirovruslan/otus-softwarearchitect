from sqlalchemy import Column, BigInteger, String

from app.db import db


class OrderStore(db.Model):
    __tablename__ = "store_orders"

    class Status:
        COMPLETED = 'completed'
        CANCELED = 'canceled'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    status = Column(String, nullable=False)
    order_id = Column(BigInteger, nullable=False)
