"""
    This module includes the APIToken class which will be used by
    SQLalchemy ORM.
"""
import datetime
from database import Database
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship


class APIToken(Database.base_class):
    """ SQLalchemy APIToken table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_tokens'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('token'),
    )

    # Database columns for this table
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False,
                     default=datetime.datetime.utcnow)
    expires = Column(DateTime)
    client_id = Column(ForeignKey('api_clients.id'), nullable=False)
    user_id = Column(ForeignKey("users.id"),
                     nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    token = Column(String(32), nullable=False)

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
                '(id: {self.id}) at {hex(id(self))}>')
