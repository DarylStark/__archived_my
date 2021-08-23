"""
    This module includes the User class which will be used by
    SQLalchemy ORM.
"""
import datetime
import enum

from sqlalchemy.orm import backref, relationship
from database import Database
from passlib.hash import argon2
from sqlalchemy import (Column, DateTime, Enum, Integer, String,
                        UniqueConstraint)


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

    # Fields that need to be hidden from the API
    api_hide_fields = ['password']

    # Many-to-one relationships
    clients = relationship(
        'APIClient',
        lazy='subquery',
        back_populates='user',
        cascade='all, delete, save-update')
    tokens = relationship(
        'APIToken',
        lazy='subquery',
        back_populates='user',
        cascade='all, delete, save-update')
    tags = relationship(
        'Tag',
        lazy='subquery',
        back_populates='user',
        cascade='all, delete, save-update')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return (f'<User for "{self.username}" ' +
                '(id: {self.id}) at {hex(id(self))}>')

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
