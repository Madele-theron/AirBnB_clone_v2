#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os
import models


class State(BaseModel, Base):
    """The State class
    Attributes:
        name: input name
    """

    __tablename__ = "states"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all", backref="state")
    else:
        name = ""

        @property
        def cities(self):
            """returns the city list instead"""
            city_values = models.storage.all("City").values()
            city_list = []
            for city in city_values:
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
