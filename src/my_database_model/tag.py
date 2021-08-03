"""
    This module includes the Tag class which will be used by
    SQLalchemy ORM.
"""
from sqlalchemy.sql.schema import ForeignKey
from database import Database
from sqlalchemy import (Column, Integer, String, UniqueConstraint)


class Tag(Database.base_class):
    """ SQLalchemy tags table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tags'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('user_id', 'title'),
    )

    # Database columns for this table
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"),
                     nullable=False)
    title = Column(String(32), nullable=False)

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return f'<Tag for "{self.title}" at {self.id}>'
