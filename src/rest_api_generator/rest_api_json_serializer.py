"""
    Module that keeps the RESTAPIJSONEncoder class, which seriales
    a RESTAPIResponse to a JSON serializable object.
"""
# ---------------------------------------------------------------------
# Imports
from json import JSONEncoder
from typing import Any, Dict
from rest_api_generator.rest_api_response import RESTAPIResponse
# ---------------------------------------------------------------------


class RESTAPIJSONEncoder(JSONEncoder):
    """ Class that can be used to serialize RESTAPIResponse objects """

    def default(self, object: Any) -> Dict:
        """ The default method of the encoder gets the objects that the
            JSON encoder cannot encode. In this method, we check what
            type of object it is and create a dict of it so the JSON
            encoder can encode it.

            Parameters
            ----------
            object : Any
                The object to encode.

            Returns
            -------
            dict
                A dictionary the JSON encoder can encode.
        """

        # Check what kind of object we got
        if isinstance(object, RESTAPIResponse):
            # REST API Responses can be converted to a dict
            return self.encode_rest_api_response(object=object)
        else:
            # If we get a object that we can't encode, we raise a
            # TypeError.
            raise TypeError(
                f'Unserializable object "{object}" of type "{type(object)}"')

    def encode_rest_api_response(self, object: RESTAPIResponse) -> Dict:
        """ Method to encode a RESTAPIResponse object.

            Parameters
            ----------
            object : Any
                The object to encode.

            Returns
            -------
            dict
                A dictionary the JSON encoder can encode.
        """

        # Create a default dict that we can fill
        return_dict: Dict = {
            'success': object.success,
            'error_code': 0,
            'error_message': '',
            'data': None,
            'page': 0,
            'limit': 0,
            'last_page': 0
        }

        # If there was an error, we add error information
        if not object.success:
            return_dict['error_code'] = object.error_code
            if object.error_message:
                return_dict['error_message'] = object.error_message
        else:
            # If there wasn't a error, we remove the error fields
            return_dict.pop('error_code')
            return_dict.pop('error_message')

        # Add the data and pagination (if specified)
        return_dict['data'] = object.data
        if object.page > 0:
            return_dict['page'] = object.page
            return_dict['limit'] = object.limit
            return_dict['total_items'] = object.total_items
            return_dict['last_page'] = object.last_page

        # Return the object
        return return_dict
# ---------------------------------------------------------------------
