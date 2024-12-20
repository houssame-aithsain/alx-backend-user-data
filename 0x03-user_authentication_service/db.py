#!/usr/bin/env python3
"""
Database module for managing user records.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
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
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The hashed password for the user.

        Returns:
            User: The newly created user object.
        """
        session = self._session
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            session.add(new_user)
            session.commit()
            return new_user
        except Exception:
            session.rollback()
            raise  # Allow exceptions to propagate for better error handling

    def find_user_by(self, **filters) -> User:
        """
        Finds a user in the database using provided attributes.

        Args:
            **filters: Keyword arguments for the user attributes to search for.

        Returns:
            User: The user object matching the filters.

        Raises:
            InvalidRequestError: If any filter attribute is invalid.
            NoResultFound: If no user matches the provided filters.
        """
        session = self._session
        attributes, values = [], []

        # Validate and prepare filters
        for attribute, value in filters.items():
            if not hasattr(User, attribute):
                raise InvalidRequestError(f"Invalid attribute: {attribute}")
            attributes.append(getattr(User, attribute))
            values.append(value)

        # Execute the query
        query = session.query(User)
        user = query.filter(tuple_(*attributes).in_([tuple(values)])).first()
        if not user:
            raise NoResultFound("No user found matching the given criteria.")
        return user

    def update_user(self, user_id: int, **updates) -> None:
        """
        Updates attributes of an existing user in the database.

        Args:
            user_id (int): The ID of the user to update.
            **updates: Keyword arguments for the attributes to update.

        Raises:
            ValueError: If any update attribute is invalid.
        """
        session = self._session
        user = self.find_user_by(id=user_id)

        # Update attributes
        for attribute, value in updates.items():
            if not hasattr(User, attribute):
                raise ValueError(f"Invalid attribute: {attribute}")
            setattr(user, attribute, value)

        session.commit()
