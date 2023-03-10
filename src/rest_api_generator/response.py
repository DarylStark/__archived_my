""" This module includes the Response which represents a API response.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class ResponseType(Enum):
    """ Enum that dictates the type of API response.

        Constants
        ---------
        ERROR
            Indiciates that this is a error response.

        RESOURCE_SET
            Indicates that this response contains a list of resources
            in it's data field.

        SINGLE_RESOURCE
            Indicates that this respoonse contains one resource in it's
            data field.
    """
    ERROR = 1
    RESOURCE_SET = 2
    SINGLE_RESOURCE = 3


@dataclass
class Response:
    """ Class that represent a API response

        Members
        -------
        type : ResponseType [default=ResponseType.RESOURCE_SET]
            The type of response.

        success : bool [default=True]
            Specifies if the endpoint ran successfully.

        data : Any [default=None]
            The data returned by the endpoint. Can be of any type.

        error_code : int [default=0]
            If a error occured, this field will be filled with the
            error code.

        error_message : Optional[str] [default=None]
            The message that belongs to the error.

        paginate : bool [default=True]
            Determines if this result should be paginated by the API
            generator.

        page : int [default=0]
            The pagenumber the user is on.

        limit : int [default=0]
            The maximum number of items on one page.

        last_page : int [default=0]
            The maximum page for the resource.

        runtime : float [default=0]
            The amount of miliseconds the endpoint has run.
    """

    # Mandatory members
    type: ResponseType = ResponseType.RESOURCE_SET
    success: bool = True
    data: Optional[Any] = None

    # Error data
    error_code: int = 0
    error_message: Optional[str] = None

    # Paginatoin
    paginate: bool = True
    page: int = 0
    total_items: int = 0
    limit: int = 0
    last_page: int = 0

    # Other fields
    runtime: float = 0
