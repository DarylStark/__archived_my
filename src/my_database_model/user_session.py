""" This module includes the UserSession class which will be used by
    SQLalchemy ORM. """

import datetime
import random
import string

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from database import Database


class UserSession(Database.base_class):
    """ SQLalchemy user session table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'user_sessions'

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    created = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow)
    user_id = Column(
        ForeignKey("users.id"),
        nullable=False)
    secret = Column(
        String(64),
        nullable=False)
    title = Column(
        String(128),
        nullable=True)
    host = Column(
        String(128),
        nullable=True)

    # One-to-many relationships
    user = relationship(
        'User',
        lazy='subquery',
        back_populates='user_sessions')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return (f'<UserSession for "{self.user_id}" ' +
                f'(id: {self.id}) at {hex(id(self))}>')

    def set_random_secret(
            self,
            min_length: int = 32,
            max_length: int = 64) -> str:
        """ Method to set a random secret for the usersession.

            Parameters
            ----------
            min_length : int [default=32]
                The minimum lenght of the secret

            max_length : int [default=64]
                The maximum lenght of the secret

            Returns
            -------
            str
                The generated secret.
        """

        # Generate a random password for this user
        characters = string.ascii_letters
        characters += string.digits
        characters += string.punctuation
        length = random.randint(min_length, max_length)
        random_secret = [random.choice(characters)
                         for i in range(0, length)]
        random_secret = ''.join(random_secret)

        # Set the password for the user
        self.secret = random_secret

        # Return the created password
        return random_secret
