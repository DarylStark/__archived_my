"""
    Module that keeps the RESTAPIJSONEncoder class, which seriales
    a RESTAPIResponse to a JSON serializable object.
"""
# ---------------------------------------------------------------------
# Imports
from datetime import datetime
from enum import Enum
from json import JSONEncoder
from typing import Any, Dict, Union
from database.database import Database
from rest_api_generator.response import Response, ResponseType
# ---------------------------------------------------------------------


class RESTAPIJSONEncoder(JSONEncoder):
    """ Class that can be used to serialize RESTAPIResponse objects """

    def default(self, object: Any) -> Union[Dict, int, str]:
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

            int
                A integer that the JSON encoder can use.

            str
                A string that the JSON encoder can use.
        """

        # Check what kind of object we got
        if isinstance(object, Response):
            # REST API Responses can be converted to a dict
            return self.encode_rest_api_response(object=object)
        elif isinstance(object, ResponseType):
            # ResponseTypes can be converted to a integer
            return object.value
        elif isinstance(object, Database.base_class):
            # Return the dict for the SQLalchemy object
            return self.encode_sqlalchemy_object(object=object)
        elif isinstance(object, datetime):
            return object.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(object, Enum):
            return object.value
        else:
            # If we get a object that we can't encode, we raise a
            # TypeError.
            raise TypeError(
                f'Unserializable object "{object}" of type "{type(object)}"')

    def encode_rest_api_response(self, object: Response) -> Dict:
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
            'type': object.type,
            'success': object.success,
            'error_code': 0,
            'error_message': '',
            'data': None,
            'page': 0,
            'limit': 0,
            'last_page': 0,
            'total_items': 0,
            'runtime': 0.0
        }

        # If there was an error, we add error information
        if not object.success:
            return_dict['error_code'] = object.error_code
            if object.error_message:
                return_dict['error_message'] = object.error_message

            # Remove the unneeded fields
            return_dict.pop('data')
            return_dict.pop('page')
            return_dict.pop('limit')
            return_dict.pop('last_page')
            return_dict.pop('total_items')
        else:
            # If there wasn't a error, we remove the error fields
            return_dict.pop('error_code')
            return_dict.pop('error_message')

            # Add the data and pagination (if specified)
            return_dict['data'] = object.data
            if object.type == ResponseType.RESOURCE_SET:
                return_dict['page'] = object.page
                return_dict['limit'] = object.limit
                return_dict['total_items'] = object.total_items
                return_dict['last_page'] = object.last_page
            elif object.type == ResponseType.SINGLE_RESOURCE:
                return_dict.pop('page')
                return_dict.pop('limit')
                return_dict.pop('total_items')
                return_dict.pop('last_page')

        # Add other fields
        return_dict['runtime'] = round(object.runtime, 3)

        # Return the object
        return return_dict

    def encode_sqlalchemy_object(self, object: Database.base_class):
        """ Method to encode a SQLalchemy object.

            Parameters
            ----------
            object : Database.base_class
                A object created from a subclass of
                Database.base_class.

            Returns
            -------
            dict
                A dictionary the JSON encoder can encode.
        """

        # Get the fields that we should hide
        try:
            fields_to_hide = object.api_hide_fields
        except AttributeError:
            fields_to_hide = list()

        # Get the columns
        columns = [column.name for column in type(object).__table__.columns]

        # Then we create a dict with the only the column items
        column_dict = {
            key: value
            for key, value in object.__dict__.items()
            if key in columns and key not in fields_to_hide
        }

        # Add fields that are in the 'api_extra_fields' list
        try:
            api_extra_fields = object.api_extra_fields
        except AttributeError:
            api_extra_fields = list()

        # Loop through the extra fields and add them to the outgoing dict
        for extra_field in api_extra_fields:
            try:
                column_dict[extra_field] = object.__getattribute__(extra_field)
            except AttributeError:
                column_dict[extra_field] = None

        # And we return that dict
        return column_dict

# ---------------------------------------------------------------------
