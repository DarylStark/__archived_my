""" This module includes the APITokenScope class which will be used by
    SQLalchemy ORM. """

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Database


class APITokenScope(Database.base_class):
    """ SQLalchemy APITokenScope table """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_token_scopes'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('token_id', 'scope_id'),
    )

    # Database columns for this table
    id = Column(
        Integer,
        primary_key=True)
    token_id = Column(
        ForeignKey('api_tokens.id'),
        nullable=False)
    scope_id = Column(
        ForeignKey('api_scopes.id'),
        nullable=False)

    # Many-to-one relationships
    token = relationship(
        'APIToken',
        lazy='subquery',
        back_populates='token_scopes')
    scope = relationship(
        'APIScope',
        lazy='subquery',
        back_populates='token_scopes')

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return (f'<APITokenScope for "{self.token_id}.{self.scope_id}" ' +
                f'(id: {self.id}) at {hex(id(self))}>')
