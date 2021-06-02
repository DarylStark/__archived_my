"""
    Module that contains the methods to get API authentication details
    from the database
"""
# ---------------------------------------------------------------------
# Imports
from typing import Optional
from my_database import db
from database_my_model import APIToken
# ---------------------------------------------------------------------
# Methods


def get_token_information(token: str) -> Optional[APIToken]:
    # # session.query(APIToken).filter(APIToken.token == 'poiuytrewq').first()
    print(db)
    pass
# ---------------------------------------------------------------------
