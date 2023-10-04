#!/usr/bin/python3
"""The state class"""

from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """
    Class representing a state in the system.

    Attributes:
        __tablename__ (str): The name of the database table for states.
        name (str): The name of the state.
        cities (list): A list of City objects associated with this state.

    Methods:
        cities (property): Get a list of cities associated with this state.

    Relationships:
        cities (relationship): to the City model with cascade deletion.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        all_states = models.storage.all()
        cities_list = []
        matching_cities = []

        for key in all_states:
            city_data = key.replace('.', ' ')
            city_data = shlex.split(city_data)

            if city_data[0] == 'City':
                cities_list.append(all_states[key])

        for matching_city in cities_list:
            if matching_city.state_id == self.id:
                matching_cities.append(matching_city)

        return matching_cities
