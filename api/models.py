from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    stock_qty = Column(Integer, default=0)
    slot_no = Column(String(10))
    image_url = Column(String(500))


class MoneyStock(Base):
    __tablename__ = "money_stock"

    id = Column(Integer, primary_key=True)
    denom = Column(Integer)        
    quantity = Column(Integer)   
    type = Column(String(10)) 


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    paid_amount = Column(Integer)
    change_amount = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product")

