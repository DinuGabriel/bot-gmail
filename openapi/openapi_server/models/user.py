# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class User(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, user_mail=None, key_words=None):  # noqa: E501
        """User - a model defined in OpenAPI

        :param user_mail: The user_mail of this User.  # noqa: E501
        :type user_mail: str
        :param key_words: The key_words of this User.  # noqa: E501
        :type key_words: List[str]
        """
        self.openapi_types = {
            'user_mail': str,
            'key_words': List[str]
        }

        self.attribute_map = {
            'user_mail': 'userMail',
            'key_words': 'keyWords'
        }

        self._user_mail = user_mail
        self._key_words = key_words

    @classmethod
    def from_dict(cls, dikt) -> 'User':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The user of this User.  # noqa: E501
        :rtype: User
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_mail(self):
        """Gets the user_mail of this User.


        :return: The user_mail of this User.
        :rtype: str
        """
        return self._user_mail

    @user_mail.setter
    def user_mail(self, user_mail):
        """Sets the user_mail of this User.


        :param user_mail: The user_mail of this User.
        :type user_mail: str
        """
        if user_mail is None:
            raise ValueError("Invalid value for `user_mail`, must not be `None`")  # noqa: E501

        self._user_mail = user_mail

    @property
    def key_words(self):
        """Gets the key_words of this User.


        :return: The key_words of this User.
        :rtype: List[str]
        """
        return self._key_words

    @key_words.setter
    def key_words(self, key_words):
        """Sets the key_words of this User.


        :param key_words: The key_words of this User.
        :type key_words: List[str]
        """

        self._key_words = key_words
