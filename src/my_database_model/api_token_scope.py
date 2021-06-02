"""
    This module includes the APITokenScope class which will be used by
    SQLalchemy ORM.
"""
# ---------------------------------------------------------------------
# Imports
import datetime
from sqlalchemy import Column, Integer, DateTime, String, UniqueConstraint, \
    ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Database
# ---------------------------------------------------------------------


class APITokenScope(Database.base_class):
    """ SQLalchemy APITokenScope table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_token_scopes'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('token_id', 'scope_id'),
    )

    # Database columns for this table
    id = Column(Integer, primary_key=True)
    token_id = Column(ForeignKey('api_tokens.id'), nullable=False)
    scope_id = Column(ForeignKey('api_scopes.id'), nullable=False)

    # One-to-one relationships
    token = relationship('APIToken', backref='scopes')
    scope = relationship('APIScope', backref='scopes')

# ---------------------------------------------------------------------
