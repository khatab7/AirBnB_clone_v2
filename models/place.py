#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.review import Review
import models
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id', ondelete='CASCADE'),
                     nullable=False)
    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", cascade="all, delete",
                               backref="place", passive_deletes=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        @property
        def reviews(self):
            """Return the list of reviews"""
            list_reviews = []
            for value in models.storage.all(Review).values():
                if value.place_id == self.id:
                    list_reviews.append(value)
            return list_reviews