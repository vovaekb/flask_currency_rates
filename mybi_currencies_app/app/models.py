from sqlalchemy import Column, Integer
from sqlalchemy.types import Date, Float
from app import database # import Base

class CurrencyRate(database.Base):
    __tablename__ = 'currency_rates'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date())
    nominal = Column(Integer())
    value = Column(Float())
