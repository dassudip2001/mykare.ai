from sqlalchemy import Column, Integer, String, ForeignKey

from src.config.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    appointments = relationship("Appointment", back_populates="user")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    status = Column(String, default="booked")
    user = relationship("User", back_populates="appointments") 
