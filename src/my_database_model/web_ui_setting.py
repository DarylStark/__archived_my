""" This module includes the WebUISetting class which will be used by
    SQLalchemy ORM. """

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from database import Database


class WebUISetting(Database.base_class):
    """ SQLalchemy web ui settings table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'web_ui_settings'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('user_id', 'setting'),
    )

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    user_id = Column(
        ForeignKey("users.id"),
        nullable=False)
    setting = Column(
        String(32),
        nullable=False)
    value = Column(
        String(32),
        nullable=False)

    # One-to-many relationships
    user = relationship(
        'User',
        lazy='subquery',
        back_populates='web_ui_settings')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return f'<WebUISetting for "{self.setting}" (id: {self.id}) at {hex(id(self))}>'
