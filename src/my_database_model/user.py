"""
    This module includes the User class which will be used by
    SQLalchemy ORM.
"""
# ---------------------------------------------------------------------
# Imports
import datetime
import enum
from passlib.hash import argon2
from sqlalchemy import Column, Integer, DateTime, String, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from database import Database
# ---------------------------------------------------------------------


class UserRole(enum.Enum):
    """ Enum containing the roles a user can have. """

    root = 1
    admin = 2
    user = 3


class User(Database.base_class):
    """ SQLalchemy user table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'users'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('email')
    )

    # Database columns for this table
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False,
                     default=datetime.datetime.utcnow)
    fullname = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    password = Column(String(512), nullable=False)
    password_date = Column(DateTime, nullable=False)

    def set_password(self, password: str) -> None:
        """ Method to set the password for this user

            Parameters
            ----------
            password : str
                The password to set for the user

            Returns
            -------
            None
        """
        self.password = argon2.hash(password)
        self.password_date = datetime.datetime.utcnow()

    def verify_password(self, password: str) -> bool:
        """ Checks the password and returns True if the given password

            is correct
            Parameters
            ----------
            password : str
                The password to verify

            Returns
            -------
            bool
                True if the password is correct, False if the password
                is not correct
        """
        return argon2.verify(password, self.password)

# ---------------------------------------------------------------------
