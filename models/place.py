#!/usr/bin/python3
""" Place Module for HBNB project """
#8from sqlalchemy import (Column, String, 
#8                        ForeignKey, Float, 
#8                        Integer)
from models.base_model import BaseModel #8, Base


class Place(BaseModel):#BASE8
    """ A place to stay """

    __tablename__ = 'places'
    city_id = ""#8Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = ""#8Column(String(60), ForeignKey('users.id'), nullable=False)
    name = ""#8Column(String(128), nullable=False)
    description = ""#8Column(String(1024))
    number_rooms = 0#8Column(Integer, default=0)
    number_bathrooms = 0#8Column(Integer, default=0)
    max_guest = 0#8Column(Integer, default=0)
    price_by_night = 0#8Column(Integer, default=0)
    latitude = 0.0#8Column(Float)
    longitude = 0.0#8Column(Float)
    amenity_ids = []