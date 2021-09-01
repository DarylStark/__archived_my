# REST API Generator

The REST API Generator package is a package that contains a class that can be used to generate a REST API. The object can be used with Flask as it exposed a Flask Blueprint. By using this package, a REST API can be created quickly with authorization.

## Usage

To use the package, you create a object of the RESTAPIGenerator class. Each API consists of groups, which in turn consist of endpoint or subgroups. A endpoint contains the specific code to run a certain task. For instance, you can create a API that contains a group with the name 'users'. This group can, in turn, have a endpoint named 'groups' that can be used to create, retrieve, update and delete user groups.

### Example

The following code is an example to create a REST API that contains a group with the name 'users', which contains one endpoint:

```python
from flask import Flask
from rest_api_generator import RESTAPIGenerator, Group, Response
from rest_api_generator import Authorization, ResponseType

def authorization(auth: str, permissions: Optional[List[str]]) -> Authorization:
    """ Authorization method for the REST API """

    # For the example, we always return a 'True' value. In a production
    # environment, you should use the authorization object and the 
    # given scopes to verify if the user is authorized to run this
    # endpoint
    auth = Authorization()
    auth.authorized = True

    # Set a 'data' object. We set this to a empty dict for now, but in
    # the real software, you can set this to, for example, a user
    # object. The returned RESTAPIAuthorized object will be passed to
    # the endpoint, so it can use the data to check what resources to
    # return for the user.
    auth.data = {}

    # Return the created object
    return auth

# Create a Flask object
flask_app = Flask(__name__)

# Create a RESTAPIGenerator object
my_rest_api_v1 = RESTAPIGenerator(
    bp_name='my_rest_api_v1',
    bp_import_name=__name__,
    bp_url_prefix='/api/v1/')

# Turn on authorization
my_rest_api_v1.use_authorization = True
my_rest_api_v1.authorization_function = authorization

# Make sure errors get reported as JSON error resposne instead of
# normal Flask error pages
my_rest_api_v1.abort_on_error = False

# Enable the correct methods
my_rest_api_v1.accept_method('POST')
my_rest_api_v1.accept_method('PATCH')
my_rest_api_v1.accept_method('DELETE')

# Create a Group for users
api_group_users = Group(
    api_url_prefix='users',
    name='api',
    description='Contains endpoints for users'
)

# Add a 'users' endpoint
@api_group_users.register_endpoint(
    url_suffix=['users', 'users/'],
    http_methods=['GET'],
    name='users',
    description='Endpoint to retrieve users',
    auth_needed=True,
    auth_scopes=EndpointPermissions(GET=['users.retrieve'])
)
def users(auth: Optional[Authorization],
          url_match: re.Match) -> Response:
    """ 'users' endpoint """
    
    # Create a response object
    retval = Response()
    retval.data = [
        { 'id': 10, 'username': 'daryl.stark' },
        { 'id': 11, 'username': 'test.user1' },
        { 'id': 12, 'username': 'test.user2' },
    ]

    return retval

# Register the created groups
my_rest_api_v1.register_group(group=api_group_api)

# The RESTAPIGenerator object works with a Blueprint object that can be
# added to the Flask app. By doing this.
flask_app.register_blueprint(my_rest_api_v1.blueprint)
```

After creating this code, the 'users' endpoint is available on `<url>/api/v1/users/users` and will return a JSON object with the generated data, a success key and runtime information.