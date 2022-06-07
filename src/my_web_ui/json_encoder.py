""" Module that keeps the WebUIJSONEncoder class, which seriales
    a Response to a JSON serializable object. """

from datetime import date, datetime
from enum import Enum
from json import JSONEncoder
from typing import Any, Dict, Union
from database.database import Database
from my_web_ui.response import Response


class WebUIJSONEncoder(JSONEncoder):
    """ Class that can be used to serialize Response objects """

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
        elif isinstance(object, Database.base_class):
            # Return the dict for the SQLalchemy object
            return self.encode_sqlalchemy_object(object=object)
        elif isinstance(object, datetime):
            return object.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(object, date):
            return object.strftime('%Y-%m-%d')
        elif isinstance(object, Enum):
            return object.value
        else:
            # If we get a object that we can't encode, we raise a
            # TypeError.
            raise TypeError(
                f'Unserializable object "{object}" of type "{type(object)}"')

    def encode_rest_api_response(self, object: Response) -> Dict:
        """ Method to encode a Response object.

            Parameters
            ----------
            object : Response
                The object to encode.

            Returns
            -------
            dict
                A dictionary the JSON encoder can encode.
        """

        # Create a default dict that we can fill
        return_dict: Dict = {
            'success': object.success,
            'error_code': object.error_code,
            'data': object.data,
        }

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

        # Get the fields that we just have to set to True if they are set
        try:
            fields_to_mask = object.api_mask_fields
        except AttributeError:
            fields_to_mask = list()

        # Get the columns
        columns = [column.name for column in type(object).__table__.columns]

        # Then we create a dict with the only the column items
        column_dict = {
            key: value
            for key, value in object.__dict__.items()
            if key in columns and key not in fields_to_hide
        }

        # Then, we mask all the fields that should be masked
        for field in fields_to_mask:
            if field in column_dict.keys():
                column_dict[field] = column_dict[field] != None

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
