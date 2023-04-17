""" The my_database_model will contain the complete database model for
    the project. """
from database.database import Database
from my_database_model.api_client import APIClient
from my_database_model.api_scope import APIScope
from my_database_model.api_token import APIToken
from my_database_model.api_token_scope import APITokenScope
from my_database_model.date_tag import DateTag
from my_database_model.note import Note
from my_database_model.note_folder import NoteFolder
from my_database_model.tag import Tag
from my_database_model.user import User, UserRole
from my_database_model.user_session import UserSession
from my_database_model.web_ui_setting import WebUISetting
