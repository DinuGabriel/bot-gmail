# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.user import User  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_user(self):
        """Test case for add_user

        Add new user
        """
        user = openapi_server.User()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/task',
            method='POST',
            headers=headers,
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_getuser_mail(self):
        """Test case for getuser_mail

        Get mail adress
        """
        query_string = [('userMail', 'examplemailadress@gmail.com')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/task',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
