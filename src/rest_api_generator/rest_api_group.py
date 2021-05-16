"""
    This module includes the RESTAPIGroup which represents a API group.
"""
# ---------------------------------------------------------------------


class RESTAPIGroup:
    """ Class that represent a API group """

    def __init__(self):
        """ The initiator sets a empty list of endpoint """

        self.endpoints = list()

    def register_endpoint(self, method):
        """ Decorator to register a endpoint for this REST API group
        """

        # Add the endpoint to the list
        self.endpoints.append(method)
# ---------------------------------------------------------------------
