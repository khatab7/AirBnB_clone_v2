#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity class"""

    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
<<<<<<< HEAD
    place_amenity = relationship('Place', secondary='place_amenity', viewonly=True)
=======
    place_amenity = relationship('Place', secondary='place_amenity',
                                  viewonly=True)
>>>>>>> ec2736b9637a31640e1d16711a852b1eda308300
