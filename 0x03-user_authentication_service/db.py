#!/usr/bin/env python3
"""
DB module for interacting with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    Handles interactions with the database.
    """

    def __init__(self) -> None:
        """Initializes the DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Creates or retrieves the session."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The hashed password.

        Returns:
            User: The created user.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by the given criteria.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first matching user.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except TypeError:
            raise InvalidRequestError
