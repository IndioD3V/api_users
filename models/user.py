from sqlalchemy import Column, Integer, String, Date, DateTime, VARCHAR, func
from .base import Base



class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), index=True, nullable=False)
    email = Column(VARCHAR(120), unique=True, index=True, nullable=False)
    phone = Column(VARCHAR(14))
    birthday = Column(Date, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    cpf = Column(VARCHAR(14), index=True,unique=True, nullable=False)
    updated_at = Column(DateTime)
    address = Column(VARCHAR(120))