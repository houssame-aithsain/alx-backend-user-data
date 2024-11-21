#!/usr/bin/env python3
"""
For users
"""

from sqlalchemy import create_engine
from sqlalchemy import declarative_base
from sqlalchemy import Column, Integer, String
# id, the integer primary key
# email, a non-nullable string
# hashed_password, a non-nullable string
# session_id, a nullable string
# reset_token, a nullable string


engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class user(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    reset_token = Column(String, nullable=False)
