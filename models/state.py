#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref="state",
                          cascade="all, delete, delete-orphan")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """public getter method cities to return the list
            of City objects from storage linked to the current State
            """
            storage_list = models.storage.all()
            cities_list = []
            result = []

            for key in storage_list:
                model_name = key.split('.')[0]
                if model_name == 'City':
                    cities_list.append(storage_list[key])

            for city in cities_list:
                if city.state_id == self.id:
                    result.append(city)

            return result
