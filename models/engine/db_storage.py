#!/usr/bin/python3
"""Database storage engine using SQLAlchemy"""
import json
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database Storage - creates tables"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the object"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                os.getenv("HBNB_MYSQL_USER"),
                os.getenv("HBNB_MYSQL_PWD"),
                os.getenv("HBNB_MYSQL_HOST"),
                os.getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """All"""
        dic = {}
        temp = []

        if cls is not None:
            temp = self.__session.query(cls).all()
        else:
            temp += self.__session.query(User).all()
            temp += self.__session.query(State).all()
            temp += self.__session.query(City).all()
            temp += self.__session.query(Amenity).all()
            temp += self.__session.query(Place).all()
            temp += self.__session.query(Review).all()
        for obj in temp:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            dic[key] = obj

        return dic

    def new(self, obj):
        """New"""
        try:
            self.__session.add(obj)
        except:
            pass

    def save(self):
        """Save"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload"""
        Base.metadata.create_all(self.__engine)
        current = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(current)

    def close(self):
        """Remove current session if active"""
        self.__session.remove()
