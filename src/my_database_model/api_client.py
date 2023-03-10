""" This module includes the APIClient class which will be used by
    SQLalchemy ORM. """

import datetime
import random
import string
from typing import Optional

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from database import Database


class APIClient(Database.base_class):
    """ SQLalchemy APIClient table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_clients'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('app_name', 'app_publisher', 'user_id'),
        UniqueConstraint('token')
    )

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    created = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow)
    expires = Column(
        DateTime)
    user_id = Column(
        ForeignKey('users.id'),
        nullable=False)
    enabled = Column(
        Boolean,
        default=True,
        nullable=False)
    app_name = Column(
        String(64),
        nullable=False)
    app_publisher = Column(
        String(64),
        nullable=False)
    token = Column(
        String(32),
        nullable=False)
    redirect_url = Column(
        String(1024),
        nullable=True)

    # Many-to-one relationships
    user = relationship(
        'User',
        lazy='subquery',
        back_populates='clients')

    # One-to-many relationships
    tokens = relationship(
        'APIToken',
        lazy='subquery',
        back_populates='client',
        cascade='all, delete, save-update')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return (f'<APIClient for "{self.app_name}" ' +
                f'(id: {self.id}) at {hex(id(self))} >')

    def generate_random_token(self, force: bool = False) -> Optional[str]:
        """
            Method to generate a random token for this API client.

            Parameters
            ----------
            force : bool = False
                If True, this function will also generate a random
                token if a token has already been configred.

            Returns
            -------
            str
                The generated token

            None
                No token generated because one is already set.
        """
        if self.token is None or force:
            # Generate random token
            characters = string.ascii_letters
            characters += string.digits
            length = random.randint(32, 32)
            random_token = [random.choice(characters)
                            for i in range(0, length)]
            random_token = ''.join(random_token)
            self.token = random_token
            return random_token
