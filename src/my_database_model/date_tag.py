""" This module includes the DateTag class which will be used by
    SQLalchemy ORM. """

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database import Database
from sqlalchemy import (Column, Integer, Date, UniqueConstraint)


class DateTag(Database.base_class):
    """ SQLalchemy date_tags table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'date_tags'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('date', 'tag_id'),
    )

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    date = Column(
        Date,
        nullable=False)
    tag_id = Column(
        ForeignKey("tags.id"),
        nullable=False)

    # One-to-many relationships
    tag = relationship(
        'Tag',
        lazy='subquery',
        back_populates='date_tags')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return f'<DateTag for "{self.tag.title}" (id: {self.id}) at {hex(id(self))}>'
