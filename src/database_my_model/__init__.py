"""
    The database_my_model will contain the complete database model for
    the project.
"""
# ---------------------------------------------------------------------
# Import the Database class from the Database package
from database.database import Database

# Database tables
from database_my_model.api_client import APIClient
from database_my_model.api_scope import APIScope
from database_my_model.api_token import APIToken
from database_my_model.api_token_scope import APITokenScope
from database_my_model.user import UserRole, User
# ---------------------------------------------------------------------
