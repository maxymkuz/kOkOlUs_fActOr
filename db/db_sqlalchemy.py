# import sqlalchemy as db
#
# from sqlalchemy import Column, String, Integer, Date
#
# from base import Base
#
#
# # engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
#
#
# class Product(Base):
#     __tablename__ = 'asr'
#     id=Column(Integer, primary_key=True)
#     title=Column('title', String(32))
#     in_stock=Column('in_stock', Boolean)
#     quantity=Column('quantity', Integer)
#     price=Column('price', Numeric)
#
#