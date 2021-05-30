"""
    This module includes the APIScope class which will be used by
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


class APIScope(Database.base_class):
    """ SQLalchemy APIScope table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_scopes'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('module', 'subject'),
    )

    # Database columns for this table
    id = Column(Integer, primary_key=True)
    module = Column(String(32), nullable=False)
    subject = Column(String(32), nullable=False)

# ---------------------------------------------------------------------
