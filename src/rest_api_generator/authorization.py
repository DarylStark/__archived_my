"""
    This module includes the Authorization class, which can be used to
    identify if a user is authorized to do something.
"""
# ---------------------------------------------------------------------
# Imports
from dataclasses import dataclass
from typing import Any, List, Optional
# ---------------------------------------------------------------------


@dataclass
class Authorization:
    """ Class that can be used to identify a authorization.

        Members
        -------
        authorized : bool
            Identifies if a request is authorized or not.

        data : Any
            Any type of data that the client wants to append. Can be,
            for example, a user object identifing the user.
    """

    authorized: bool = False
    data: Any = None
# ---------------------------------------------------------------------
