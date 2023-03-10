""" This module includes the APIScope class which will be used by
    SQLalchemy ORM. """

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Database


class APIScope(Database.base_class):
    """ SQLalchemy APIScope table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_scopes'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('module', 'subject'),
    )

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    module = Column(
        String(32),
        nullable=False)
    subject = Column(
        String(32),
        nullable=False)

    # One-to-many relationships
    token_scopes = relationship(
        'APITokenScope',
        lazy='subquery',
        back_populates='scope',
        cascade='all, delete, save-update')

    def __repr__(self):
        """ Represents objects of this class. """
        return (f'<APIScope for "{self.module}.{self.subject}" ' +
                '(id: {self.id}) at {hex(id(self))}>')

    @property
    def full_scope_name(self) -> str:
        """ Method that creates a 'full API scope' object. """
        return f'{self.module}.{self.subject}'
