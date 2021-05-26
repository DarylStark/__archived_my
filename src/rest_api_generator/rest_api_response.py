"""
    This module includes the RESTAPIResponse which represents a API
    response.
"""
# ---------------------------------------------------------------------
from typing import Any, Optional
from dataclasses import dataclass
from enum import Enum
# ---------------------------------------------------------------------


class ResponseType(Enum):
    """ Enum that dictates the type of API response.

        Constants
        ---------
        RESOURCE_SET
            Indicates that this response contains a list of resources
            in it's data field.

        SINGLE_RESOURCE
            Indicates that this respoonse contains one resource in it's
            data field.
    """
    RESOURCE_SET = 1
    SINGLE_RESOURCE = 2


@dataclass
class RESTAPIResponse:
    """ Class that represent a API response

        Members
        -------
        success : bool
            Specifies if the endpoint ran successfully.

        data : Any
            The data returned by the endpoint. Can be of any type.

        error_code : int
            If a error occured, this field will be filled with the
            error code.

        error_message : str
            The message that belongs to the error.

        paginate : bool
            Determines if this result should be paginated by the API
            generator.

        page : int
            The pagenumber the user is on.

        limit : int
            The maximum number of items on one page.

        last_page : int
            The maximum page for the resource.
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
# ---------------------------------------------------------------------
