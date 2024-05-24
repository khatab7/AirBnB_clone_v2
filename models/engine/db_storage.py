#!/usr/bin/python3
"""This is the file storage class for AirBnB"""

#from models.base_model import Base
from models.base_model import Base, BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from os import getenv


class DBStorage:
    """ Storage for database with SQL Alchemy and MySQL """
    __engine = None
    __session = None

    def __init__(self):
        """ Constructor """

        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(username, password, host, db_name)

        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session (self.__session)
        all objects depending of the class name (argument cls)
        """

        session = self.__session
        ob_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                ob_list = self.__session.query(cls).all()
        else:
            for sub in Base.__subclasses__():
                ob_list.extend(self.__session.query(sub).all())
        ob_dict = {}
        for obj in ob_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            try:
                del obj._sa_instance_state
                ob_dict[key] = obj
            except Exception:
                pass
        return ob_dict

    def new(self, obj):
        """ add the object to the current database session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from module import symbol
        the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        creates all tables in the database
        creates the current database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes Session
        """
        self.__session.close()