""" This module includes the Response which represents a backend
    response. """

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Response:
    """ Class that represent a backend respons

        Members
        -------
        success : bool [default=True]
            Specifies if the query ran successfully.

        data : Dict [default=None]
            The data returned by the backend. Should always be a dict

        error_code : int [default=0]
            If a error occured, this field will be filled with the
            error code.
    """

    # Mandatory members
    success: bool = False
    data: Optional[Dict] = None

    # Error data
    error_code: Optional[int] = None
