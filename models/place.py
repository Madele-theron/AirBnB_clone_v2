#!/usr/bin/python3
"""The Place class"""
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models

if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False,
        ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False,
        ),
    )


class Place(BaseModel, Base):
    """The Place class"""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "places"

        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            backref="place_amenities",
        )
        reviews = relationship("Review", cascade="all, delete", backref="places")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        """Returns a list of Reviews instances"""
        review_values = models.storage.all("Review").values()
        review_list = []
        for review in review_values:
            if review.place_id == self.id:
                review_list.append(review)
        return review_list

    @amenities.setter
    def amenities(self, value):
        """Appends amenity ids to the attribute"""
        if isinstance(value, Amenity):
            self.amenity_ids.append(value.id)

    if getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def amenities(self):
            """attribute that returns the list of Amenity instances"""
            amenity_values = models.storage.all("Amenity").values()
            amenity_list = []
            for amenity in amenity_values:
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
