#!/usr/bin/env python3
"""Mapping for user"""
from sqlalchemy import VARCHAR, Column, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Defines A user Mapping"""
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(VARCHAR(250), nullable=False)
    hashed_password = Column(VARCHAR(250), nullable=False)
    session_id = Column(VARCHAR(250))
    reset_token = Column(VARCHAR(250))
