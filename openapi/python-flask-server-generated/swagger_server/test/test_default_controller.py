# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_user(self):
        """Test case for add_user

        Add new user
        """
        body = User()
        response = self.client.open(
            '/task',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_getuser_mail(self):
        """Test case for getuser_mail

        Get mail adress
        """
        query_string = [('user_mail', 'user_mail_example')]
        response = self.client.open(
            '/task',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
