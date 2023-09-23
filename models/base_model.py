#!/usr/bin/python3
"""This is the base_model class for AirBnB_v2"""

from sqlalchemy.ext.declarative import declarative_base
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseModel:
    """This class will defines all common attributes
    for other classes
    """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance of the BaseModel class.

        Args:
            args: Unused positional arguments.
            kwargs: Keyword arguments for the constructor of the BaseModel.

        Attributes:
            id (str): A unique identifier generated for the instance.
            created_at (datetime): The date and time instance was created.
            updated_at (datetime): The date and time instance was last updated.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """instance to returns a string
        Return:
            a string of class name, id, and dictionary
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """Return a string representaion
        """
        return self.__str__()

    def save(self):
        """
        Update the instance attribute 'updated_at' to the current date & time.
        Add the current instance to the storage and save the storage data.

        This method should be called whenever changes are made to the object
        to ensure that the changes are persisted.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Convert the BaseModel instance into a dictionary representation.

        Returns:
          dict: A dictionary containing the object's attributes and metadata.
            - '__class__': The name of the class.
            - 'created_at': The creation date and time (in ISO format).
            - 'updated_at': The last update date and time (in ISO format)
        """
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict.keys():
            del my_dict['_sa_instance_state']
        return my_dict

    def delete(self):
        """ delete object
        """
        models.storage.delete(self)
