""" This module includes the APIToken class which will be used by
    SQLalchemy ORM. """

import datetime
import random
import string
from typing import Optional

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from database import Database


class APIToken(Database.base_class):
    """ SQLalchemy APIToken table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_tokens'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('token'),
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
    client_id = Column(
        ForeignKey('api_clients.id'),
        nullable=False)
    user_id = Column(
        ForeignKey("users.id"),
        nullable=False)
    enabled = Column(
        Boolean,
        default=True,
        nullable=False)
    title = Column(
        String(64),
        nullable=True)
    token = Column(
        String(32),
        nullable=False)

    # Many-to-one relationships
    client = relationship(
        'APIClient',
        lazy='subquery',
        back_populates='tokens')
    user = relationship(
        'User',
        lazy='subquery',
        back_populates='tokens')

    # One-to-many relationships
    token_scopes = relationship(
        'APITokenScope',
        lazy='subquery',
        back_populates='token',
        cascade='all, delete')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return (f'<APIToken for "{self.client_id}" ' +
                f'(id: {self.id}) at {hex(id(self))}>')

    def generate_random_token(self, force: bool = False) -> Optional[str]:
        """
            Method to generate a random token for this API token.

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
