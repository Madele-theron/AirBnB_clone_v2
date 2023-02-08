#!/usr/bin/python3
"""This is the user class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class User(BaseModel, Base):
    """This is the class for user"""

    __tablename__ = "users"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        places = relationship("Place", cascade="all", backref="user")
        reviews = relationship("Review", cascade="all", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
