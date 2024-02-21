#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add a user object to db
        Args:
            email (str): email for user
            hashed_password (str): hashed_password for user
        Returns:
            - User
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """Filter user table by kwargs
        args:
            args (array of str): not used
            kwargs (dict): key and value to filter user by
        Returns:
            - User object
        Exception:
            - NoResult
            - InvalidRequestError
        """
        for key in kwargs:
            if key not in User.__dict__:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id, **kwargs):
        """Update a user in the db identified by user_id
        user_id (int): integer identifier for  the user
        Args:
            kwargs (dict): attributes in the user to update
        Returns:
            - None (successful)
        Exception:
            - ValueError: if an argument doesn't corresponds
            to a user attribute
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, val in kwargs.items():
                if key not in User.__dict__:
                    raise ValueError
                setattr(user, key, val)
            self._session.commit()
        except (InvalidRequestError, NoResultFound):
            raise ValueError
