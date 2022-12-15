#!/usr/bin/python3
"""This module defines a class to manage the database storage for
   the hbnb clone
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """This class manages storage of hbnb models in the database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage model"""

        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(user, password, host, db), pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """queries all objects from the db depending on the class name"""

        objs = {}
        if cls is not None:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for item in query:
                key = "{}.{}".format(type(item).__name__, item.id)
                objs[key] = item
        else:
            obj_list = [User, State, City, Amenity, Place, Review]

            for class_name in obj_list:
                query = self.__session.query(class_name)
                for item in query:
                    key = "{}.{}".format(type(item).__name__, item.id)
                    objs[key] = item

        return (objs)

    def new(self, obj):
        """adds a new object to the current session"""
        self.__session.add(obj)

    def save(self):
        """saves an object to the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current session if obj is not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()

    def close(self):
        """ closes the session """
        self.__session.close()
