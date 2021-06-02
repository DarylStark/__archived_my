"""
    This module includes the APIToken class which will be used by
    SQLalchemy ORM.
"""
# ---------------------------------------------------------------------
# Imports
import datetime
from sqlalchemy import Column, Integer, DateTime, String, UniqueConstraint, \
    ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Database
from my_database_model.api_token_scope import APITokenScope
# ---------------------------------------------------------------------


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
    client = relationship('APIClient', backref='api_tokens')
    user = relationship('User', backref='api_tokens')

# ---------------------------------------------------------------------
