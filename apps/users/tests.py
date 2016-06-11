import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from django.test import Client, TestCase

from rest_framework.authtoken.views import obtain_auth_token

User = get_user_model()


class UsersURLsTestCase(TestCase):
    """
    User urls testcases
    """
    def test_get_token_url_uses_obtain_token_view(self):
        """
        Test that the get token url resolves to the correct
        view function.
        """
        get_token = resolve('/api/v1/users/get-token/')
        self.assertEqual(get_token.func, obtain_auth_token)


class UserGetTokenTestCase(TestCase):
    """
    Get token for user testcases
    """
    def setUp(self):
        self.john_password = 'johnpassword'

        self.lennon = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            self.john_password)

        self.client = Client()

    def test_get_token_with_valid_username_and_password(self):
        """
        Test that when trying to get a token with a valid username and password
        the status code is 200 and a token string it is retrieved
        """
        token_result = self.client.post('/api/v1/users/get-token/', data={
            'username': self.lennon.username,
            'password': self.john_password,
        })

        self.assertEqual(token_result.status_code, 200)

        token_result_content = token_result.content
        result_json = json.loads(token_result_content.decode('utf-8'))
        token = result_json['token']

        self.assertIsNotNone(token) and self.assertIsNot(token, "")

    def test_get_token_with_invalid_username_and_password(self):
        """
        Test that when trying to get a token with a invalid username and password
        the status code is 400 and no token is returned on the JSON.
        """
        token_result = self.client.post('/api/v1/users/get-token/', data={
            'username': self.lennon.username,
            'password': 'bad password',
        })

        token_result_content = token_result.content
        self.assertEqual(token_result.status_code, 400)

        result_json = json.loads(token_result_content.decode('utf-8'))

        self.assertEqual(result_json.get('token'), None)




