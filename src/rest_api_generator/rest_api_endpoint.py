"""
    This module includes the RESTAPIEndpoint which represents a API
    endpoint.
"""
# ---------------------------------------------------------------------
from typing import List, Optional
from dataclasses import dataclass
# ---------------------------------------------------------------------


@dataclass
class RESTAPIEndpoint:
    """ Class that represent a API endpoint

        Members
        -------
        url_suffix: str
            The URL suffix for the endpoint.

        func:
            The method / function to run for this endpoint

        name: str(default=None)
            The name for the API endpoint. Is used in help pages

        description: str(default=None)
            Description for the API endpoint. Is used in help pages

        http_methods: List[str](default=None)
            HTTP methods that this API endpoint supports
    """

    # Set the values
    url_suffix: str
    func: str
    name: Optional[str]
    description: Optional[str]
    http_methods: Optional[List[str]]
# ---------------------------------------------------------------------
