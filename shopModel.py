from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password_hash = Column(String(255))
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    quantity = Column(Integer)
    seller_id = Column(Integer, ForeignKey('users.id'))
    seller = relationship('User')
    date_create = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    date_update = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    buyer_id = Column(Integer, ForeignKey('users.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))
    quantity = Column(Integer)
    total_price = Column(DECIMAL(10, 2))
    status = Column(Boolean, default=False)
    date_create = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    date_update = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    item = relationship('Item')
    buyer = relationship('User', foreign_keys=[buyer_id])
    seller = relationship('User', foreign_keys=[seller_id])
