#!/usr/bin/python3
"""
This script defines the DBStorage class for SQLAlchemy ORM.

It provides a database storage backend for the application and manages
database connections, queries, and data manipulation.

Classes:
- DBStorage: Manages database storage and interactions.
"""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """
    Database storage manager for SQLAlchemy ORM.
    """

    def __init__(self):
        """
        Initializes a new DBStorage instance.

        Args:
            None
        """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of objects from the database.

        Args:
            cls (class, optional): A class name to filter objects.
                If provided, returns objects of the specified class.

        Returns:
            dict: A dictionary of objects with keys in the format
                'ClassName.ObjectID'.
        """

        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lista = [State, City, User, Place, Review, Amenity]
            for clase in lista:
                query = self.__session.query(clase)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return dic

    def new(self, obj):
        """
        Adds a new object to the current database session.

        Args:
            obj: The object to add to the database.
        """
        self.__session.add(obj)

    def save(self):
        """
        Saves changes to the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session.

        Args:
            obj (object, optional): The object to delete.
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """
        Reloads database tables and creates a new database session.
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """
        Closes the current database session.
        """
        self.__session.close()
