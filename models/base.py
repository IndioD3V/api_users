from sqlalchemy import Column, Integer, String, Date, DateTime, VARCHAR, func

from database import db

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)