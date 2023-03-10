""" This module includes the Tag class which will be used by
    SQLalchemy ORM. """

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from database import Database


class Tag(Database.base_class):
    """ SQLalchemy tags table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tags'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('user_id', 'title'),
    )

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    user_id = Column(
        ForeignKey("users.id"),
        nullable=False)
    title = Column(
        String(128),
        nullable=False)
    color = Column(
        String(6),
        nullable=True)

    # Many-to-one relationships
    date_tags = relationship(
        'DateTag',
        lazy='subquery',
        back_populates='tag',
        cascade='all, delete, save-update')

    # One-to-many relationships
    user = relationship(
        'User',
        lazy='subquery',
        back_populates='tags')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return f'<Tag for "{self.title}" (id: {self.id}) at {hex(id(self))}>'
