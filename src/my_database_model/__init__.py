"""
    The my_database_model will contain the complete database model for
    the project.
"""
# ---------------------------------------------------------------------
# Import the Database class from the Database package
from database.database import Database

# Database tables
from my_database_model.api_client import APIClient
from my_database_model.api_scope import APIScope
from my_database_model.api_token import APIToken
from my_database_model.api_token_scope import APITokenScope
from my_database_model.user import UserRole, User
# ---------------------------------------------------------------------