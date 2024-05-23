#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('city', backref='state', cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """

            """
            import models
            from models.city import City
            City_list = []
            for city in models.storage.all(city).values():
                if city.state_id == self.id:
                    City_list.append(city)
            return City_list