import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi.openapi_server.models.user import User  # noqa: E501
from openapi.openapi_server import util


def add_user(user=None):  # noqa: E501
    """Add new user

    This allows you to add a new user. # noqa: E501

    :param user: 
    :type user: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501

    # Function Implementation
    return f'Add user {user}'


def get_user_mail(user_mail):  # noqa: E501
    """Get mail adress

    This operation allows you to feach user mail adress. # noqa: E501

    :param user_mail: 
    :type user_mail: str

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    # Function Implementation
    return f'Get user mail for {user_mail}'
