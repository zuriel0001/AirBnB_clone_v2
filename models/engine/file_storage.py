#!/usr/bin/python3
"""This is the file storage class for AirBnB_v2"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """
    A class for managing storage and retrieval of objects to/from a JSON file.

    Attributes:
        __file_path(str): path to the JSON file
        __objects(dic): A dictionary to store objects with their unique keys.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Retrieve all objects from the internal storage dictionary.

        Args:
           cls (Optional[Type]): filter objects by the specified class.

        Returns:
           dict: A dictionary containing objects from the storage dictionary.
           If 'cls' is given, only objects of the specified class are returned.
        """
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace('.', ' ')
                partition = shlex.split(partition)
                if (partition[0] == cls.__name__):
                    dic[key] = self.__objects[key]
            return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """
        Add a new object to the internal storage dictionary.

        Args:
          obj: The object to be added.

        Returns:
           None
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
         Serialize objects from the internal storage dictionary to a JSON file.

        The method iterates through the objects in `self.__objects`,
        converts them to dictionaries using the `to_dict` method
        (assuming such a method exists for the objects), and
        saves them to the JSON file specified by `self.__file_path`.

    Returns:
        None
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """
        Load & reload objects from a JSON file into internal storage dict.

        If the file specified by `self.__file_path` exists,
        it reads the JSON data, reconstructs objects, and populates
        the internal dictionary with them.

        If the file is not found, the method does nothing.

        Returns:
            None
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete an object from the internal storage dictionary, if it exists.

        Args:
            obj: The object to be deleted. If provided, the method will attempt
             to remove the object from the storage dictionary.

        Return:
            None
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """
        Close and finalize any operations or resources related to this class.
        """
        self.reload()
