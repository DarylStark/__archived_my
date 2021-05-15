"""
    This module defines unit tests for the database model
"""
# ---------------------------------------------------------------------
# Add include path. We need to do this because we are not in the
# original path
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), os.path.pardir, os.path.pardir)) + '/src'
)
# ---------------------------------------------------------------------
# Imports
from database_my_model import User
# ---------------------------------------------------------------------


def test_user_password_verification_correct_password() -> None:
    """ Unit test for User password verification

        Creates a user objects, sets a password and verifies if the
        password can be verified
    """

    # Create the user
    test_user = User(fullname='Test User',
                     username='test.user',
                     email='test.user@dstark.nl'
                     )

    # Set the password
    test_user.set_password('test123!')

    # Check if the password is correct
    assert test_user.verify_password('test123!')


def test_user_password_verification_wrong_password() -> None:
    """ Unit test for User password verification

        Creates a user objects, sets a password and verifies if the
        object doesn't respons positive to wrong passwords
    """

    # Create the user
    test_user = User(fullname='Test User',
                     username='test.user',
                     email='test.user@dstark.nl'
                     )

    # Set the password
    test_user.set_password('test123!')

    # Check if the password is correct
    assert not test_user.verify_password('!321tset')
# ---------------------------------------------------------------------
