# Database

The database package contains a wrapper class for SQLalchemy to create a database connection for a large scale application.

## Usage

The package contains a `Database` singleton class that should be used to create a database connection and databasesessions. First you connect to the database using this class. When you want to retrieve or update information, you do so by creating a `DatabaseSession` object.

### Example

```python
from database import Database, DatabaseSession

# Create a SQLalchemy ORM object
class User(Database.base_class):
    """ SQLalchemy user table """

    __tablename__ = 'users'

    # Database columns for this table
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    username = Column(String(128), nullable=False)
    password = Column(String(512), nullable=False)


# Set the settings
username = 'daryl'
password = 'secret'
server = 'db.dstark.nl'
database = 'testdatabase'

# Create a SQLalchemy connection string
connection_string = f'mysql+pymysql://{username}:{password}@{server}/{database}'

# Connect to the database and create the tables immidiatly
Database.connect(
    connection=connection_string,
    create_tables=True
)

# Retrieve data
with DatabaseSession(
    commit_on_end=False,
    expire_on_commit=False) as session:
        data_list = session.query(User)
```