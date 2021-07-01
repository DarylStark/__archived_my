"""
    This module defines unit tests for the database model
"""
# Add include path. We need to do this because we are not in the
# original path
import sys
import os
import pytest
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), os.path.pardir, os.path.pardir)) + '/src'
)
from my_database_model import User


# Fixtures
@pytest.fixture
def fixture_test_user() -> User:
    """ Fixture to create a User object """

    return User(fullname='Test User',
                username='test.user',
                email='test.user@dstark.nl'
                )


def test_user_password_verification_correct_password(fixture_test_user: User) -> None:
    """ Unit test for User password verification

        Verifies if the checkig of a correct password results in a
        success.
    """

    # Set the password
    fixture_test_user.set_password('test123!')

    # Check if the password is correct
    assert fixture_test_user.verify_password('test123!')


def test_user_password_verification_wrong_password(fixture_test_user: User) -> None:
    """ Unit test for User password verification

        Verifies if the checkig of a incorrect password results in a
        failure
    """

    # Set the password
    fixture_test_user.set_password('test123!')

    # Check if the password is correct
    assert not fixture_test_user.verify_password('!321tset')
