""" This module includes the NoteFolder class which will be used by
    SQLalchemy ORM. """

import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from database import Database


class NoteFolder(Database.base_class):
    """ SQLalchemy note_folders table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'note_folders'

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
    parent_id = Column(
        ForeignKey("note_folders.id"),
        nullable=True)
    name = Column(
        String(256),
        nullable=False)

    # One-to-many relationships
    user = relationship(
        'User',
        lazy='subquery',
        back_populates='note_folders')
    parent = relationship(
        'NoteFolder',
        lazy='subquery')
    notes = relationship(
        'Note',
        lazy='subquery',
        back_populates='folder')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return f'<NoteFolder for "{self.name}" (id: {self.id}) at {hex(id(self))}>'
