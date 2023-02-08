#!/usr/bin/python3
"""Class BaseModel"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import uuid
import models

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """This BaseModel class defines all common attributes/methods
    for other classes"""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model class"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == "__class__":
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, DATE_FORMAT)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at, DATE_FORMAT)

    def __str__(self):
        """Returns string representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def save(self):
        """updates attribute 'updated_at' to current datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """returns a dictionary containing all keys values in __dict__"""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = self.__class__.__name__
        if "created_at" in my_dict:
            my_dict["created_at"] = self.created_at.isoformat()
        if "updated_at" in my_dict:
            my_dict["updated_at"] = self.updated_at.isoformat()
        if "reviews" in my_dict:
            my_dict.pop("reviews", None)
        if "_password" in my_dict:
            my_dict["password"] = my_dict["_password"]
            my_dict.pop("_password", None)
        if "amenities" in my_dict:
            my_dict.pop("amenities", None)
        my_dict.pop("_sa_instance_state", None)
        if not save_to_disk:
            my_dict.pop("password", None)
        return my_dict

    def delete(self):
        """Delete current instance from storage"""
        models.storage.delete(self)
