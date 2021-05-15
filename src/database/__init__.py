"""
    The database package will be a wrapper for the SQLalchemy package
    and will contain classes and methods to interact with databases.

    To use this package, you'll have to create classes that represents
    database tables, like this:

    ```python
    from sqlalchemy import Column, Integer
    from database import Database

    class ExampleTable(Database.base_class):
        # Mandatory argument for Database objects within SQLAlchemy
        __tablename__ = 'example_table'

        # Database columns for this table
        id = Column(Integer, primary_key=True)
    ```

    After that, you can use the created class like a normal
    SQLalchemy ORM object.
"""
# ---------------------------------------------------------------------
# Imports
from database.database import Database
from database.database_session import DatabaseSession
# ---------------------------------------------------------------------
if __name__ == '__main__':
    raise NotImplementedError('This file can not be used as script')
# ---------------------------------------------------------------------
