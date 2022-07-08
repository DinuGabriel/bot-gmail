import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def add_user(body=None):  # noqa: E501
    """Add new user

    This allows you to add a new user. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def getuser_mail(user_mail):  # noqa: E501
    """Get mail adress

    This operation allows you to feach user mail adress. # noqa: E501

    :param user_mail: 
    :type user_mail: str

    :rtype: User
    """
    return 'do some magic!'
