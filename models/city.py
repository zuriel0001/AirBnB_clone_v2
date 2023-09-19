#!/usr/bin/python3
"""This is the city class"""

from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel, Base):
    """
     A class representing cities in a database.

    Attributes:
        __tablename__ (str): The name of the database table for cities.
        name (Column): The name of the city (String, max length 128, not nullable).
        state_id (Column): The foreign key reference to the associated state (String, max length 60, not nullable).
        places (relationship): A relationship to associated places in the city with cascading delete options.
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", cascade='all, delete, delete-orphan',
                          backref="cities")
