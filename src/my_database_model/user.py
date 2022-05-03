""" This module includes the User class which will be used by
    SQLalchemy ORM. """

import datetime
import enum
import random
import string
from typing import Optional
from sqlalchemy.orm import backref, relationship
from database import Database
from passlib.hash import argon2
from pyotp import TOTP, random_base32
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
        UniqueConstraint('email'),
        UniqueConstraint('second_factor')
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
    second_factor = Column(String(64), nullable=True)

    # Fields that need to be hidden from the API
    api_hide_fields = ['password']

    # Fields that should be masked for the API
    api_mask_fields = ['second_factor']

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
    user_sessions = relationship(
        'UserSession',
        lazy='subquery',
        back_populates='user',
        cascade='all, delete, save-update')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return (f'<User for "{self.username}" ' +
                f'(id: {self.id}) at {hex(id(self))}>')

    def set_random_password(
            self,
            min_length: int = 24,
            max_length: int = 33) -> str:
        """ Method to set a random password for the user.

            Parameters
            ----------
            min_length : int [default=24]
                The minimum lenght of the password

            max_length : int [default=33]
                The maximum lenght of the password

            Returns
            -------
            str
                The generated password.
        """

        # Generate a random password for this user
        characters = string.ascii_letters
        characters += string.digits
        characters += string.punctuation
        length = random.randint(min_length, max_length)
        random_password = [random.choice(characters)
                           for i in range(0, length)]
        random_password = ''.join(random_password)

        # Set the password for the user
        self.set_password(random_password)

        # Return the created password
        return random_password

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

    @staticmethod
    def get_random_second_factor() -> str:
        """ Method to get a random second factor for this user. Made static
            since it can be used without an object.

            Parameters
            ----------
            None

            Returns
            -------
            str
                The random second factor
        """
        return random_base32()

    def set_random_second_factor(self) -> str:
        """ Method to set a random second factor for this user

            Parameters
            ----------
            None

            Returns
            -------
            str
                The random second factor
        """
        self.second_factor = self.get_random_second_factor()
        return self.second_factor

    def set_second_factor(self, second_factor: str) -> str:
        """ Method to set a second factor secret for this user

            Parameters
            ----------
            second_factor : str
                The second factor secret to set

            Returns
            -------
            str
                The second factor
        """
        self.second_factor = second_factor
        return second_factor

    def disable_second_factor(self) -> None:
        """ Method to disable a second factor secret for this user

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        self.second_factor = None

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

    def verify_credentials(
            self,
            password: str,
            second_factor: Optional[str] = None) -> bool:
        """ Check if the password and second factor for this user are
            correct. Can be used to verify login attempts.

            Parameters
            ----------
            password : str
                The password to verify

            second_factor : str
                The 'second factor' value to verify

            Returns
            -------
            bool
                True if the password and second factore are correct,
                False if one of these is not correct.
        """

        # Verify the given data
        password_correct = self.verify_password(password)
        second_factor_correct = True

        # Check if a second factor is needed
        if self.second_factor:
            totp = TOTP(self.second_factor)
            second_factor_correct = totp.now() == second_factor

        # Return the values
        return password_correct and second_factor_correct
