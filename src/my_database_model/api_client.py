"""
    This module includes the APIClient class which will be used by
    SQLalchemy ORM.
"""
import datetime
from database import Database
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)


class APIClient(Database.base_class):
    """ SQLalchemy APIClient table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_clients'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('app_name', 'app_publisher'),
        UniqueConstraint('token')
    )

    # Database columns for this table
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False,
                     default=datetime.datetime.utcnow)
    expires = Column(DateTime)
    user_id = Column(ForeignKey('users.id'),
                     nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    app_name = Column(String(64), nullable=False)
    app_publisher = Column(String(64), nullable=False)
    token = Column(String(32), nullable=False)
