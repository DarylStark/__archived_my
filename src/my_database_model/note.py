""" This module includes the Note class which will be used by
    SQLalchemy ORM. """

import datetime
import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from database import Database


class NoteType(enum.Enum):
    """ Enum containing the types a note can have. """

    plain = 1               # Plain text
    markdown = 2            # Markdown format


class Note(Database.base_class):
    """ SQLalchemy notes table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'notes'

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    created = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow)
    user_id = Column(
        ForeignKey("users.id"),
        nullable=False)
    folder_id = Column(
        ForeignKey("note_folders.id"),
        nullable=True)
    type = Column(
        Enum(NoteType),
        nullable=False)
    title = Column(
        String(128),
        nullable=False)
    body = Column(
        String(1073741824),
        nullable=False)

    # One-to-many relationships
    user = relationship(
        'User',
        lazy='subquery',
        back_populates='notes')
    folder = relationship(
        'NoteFolder',
        lazy='subquery',
        back_populates='notes')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return f'<Note for "{self.title}" (id: {self.id}) at {hex(id(self))}>'
