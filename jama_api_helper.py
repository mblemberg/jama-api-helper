import requests
from typing import Callable
from pprint import pprint


def log(msg: str):
    print(msg)


def exception_handler(func: Callable) -> Callable:
    """Exception handler decorator function."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f'Error calling function: {func.__name__}'
            error_msg += '\n' + str(e)
            log(error_msg)

    return inner


class JamaInterface:
    """A helper class for interacting with the Jama REST API."""

    def __init__(self, endpoint_url: str) -> object:
        self.endpoint_url = endpoint_url
        self.access_token = None

    @exception_handler
    def authenticate(
        self,
        client_id: str,
        client_secret: str
    ) -> None:
        """Authenticate an HTTP session using the API client ID and client
        secret generated in the Jama web interface.  Saves the access token
        provided by Jama in exchange for the client API credentials.  By
        default, the access token is valid for one hour."""

        req = requests.post(
            url='https://clarios.jamacloud.com/rest/oauth/token',
            params={'grant_type': 'client_credentials'},
            auth=(client_id, client_secret)
        )

        if req.ok is not True:
            raise RuntimeError('Failed to authenticate.')

        req_json = req.json()
        self.access_token = req_json['access_token']

    @exception_handler
    def get_item(
        self,
        project_id: int = None,
        item_project_id: str = None,
        item_global_id: str = None
    ) -> object:
        """Get an item specified either by the item global ID or the project
        ID and the item project ID."""

        if self.access_token is None:
            raise RuntimeError(
                'Tried to access Jama items without first authenticating.')

        if item_global_id is not None:
            req = requests.get(
                url=self.endpoint_url + '/abstractitems',
                params={
                    'documentKey': item_global_id
                }
            )

        elif project_id is not None and item_project_id is not None:
            req = requests.get(
                url=self.endpoint_url + '/abstractitems',
                params={
                    'documentKey': item_project_id,
                    'project': project_id
                },
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )

        else:
            raise RuntimeError('Error:  Item insufficiently defined.')

        return JamaItem(req)


class JamaItem:
    """Represents an item in Jama."""

    def __init__(self, response: object = None):
        response_json = response.json()
        data = response_json['data'][0]

        self.id = data['id']
        self.item_project_id = data['documentKey']
        self.global_id = data['globalId']
        self.project_id = data['project']
        self.fields: dict = data['fields']

    def __str__(self):
        """String representation of the JamaItem."""

        items = [
            f'Item Project ID: {self.item_project_id}',
            f'Item Global ID: {self.global_id}',
        ]

        if 'name' in self.fields.keys():
            items.append(f'Name: {self.fields["name"]}')

        if 'description' in self.fields.keys():
            items.append(f'Description: {self.fields["description"]}')

        return '\n'.join(items)

    def print_fields(self):
        """Pretty prints the self.fields dictionary."""

        pprint(self.fields)
