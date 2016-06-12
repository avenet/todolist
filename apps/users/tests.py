import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import Client, TestCase

from rest_framework.authtoken.views import obtain_auth_token

from .serializers import UserCreateSerializer
from .views import UserCreate

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
        Tests that when trying to get a token with a valid username and password
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
        Tests that when trying to get a token with a invalid username and password
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


class UserCreateSerializerTests(TestCase):
    """
    UserSerializer class tests
    """
    def test_user_serializer_model(self):
        """
        Test that the user serializer model is set to all of the objects from the user class
        """
        self.assertEqual(UserCreateSerializer.Meta.model, User)

    def test_user_serializer_fields(self):
        """
        Test that the user serializer fields are set correctly on the user serializer class
        """
        fields = {'username', 'password', 'email', 'first_name', 'last_name'}
        self.assertEqual(set(UserCreateSerializer.Meta.fields), fields)


class UserCreateTests(TestCase):
    def setUp(self):
        self.lennon = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword')

    @staticmethod
    def create_post_request(data):
        user_create_view = UserCreate()

        request = HttpRequest()
        request.data = data

        return user_create_view.post(request)

    def test_create_already_existing_username(self):
        """
        Tests that when trying to create an username which already exists
        the response status code is 400 and a message error appears on the
        username part.
        """
        response = self.create_post_request({
            'username': self.lennon.username,
            'password': 'test'
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'], [
            'A user with that username already exists.'
        ])

    def test_create_invalid_user_with_empty_parameters(self):
        """
        Tests that creating a user without parameters causes
        status code 400 on the response and validation errors on the response JSON
        """
        response = self.create_post_request({})

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.data['username'], [
            'This field is required.'
        ])
        self.assertEqual(response.data['password'], [
            'This field is required.'
        ])

    def test_create_valid_user(self):
        """
        Tests that creating a valid user causes status code 201
        with a user created on the database
        """
        create_user_params = {
            'username': 'mosteel',
            'password': 'test',
            'first_name': 'Clark',
            'last_name': 'Kent',
            'email': 'clark@kent.com',
        }

        response = self.create_post_request(create_user_params)

        self.assertEqual(response.status_code, 201)

        mosteel = User.objects.get(username=create_user_params.get('username'))

        self.assertEqual(mosteel.first_name, create_user_params['first_name'])
        self.assertEqual(mosteel.last_name, create_user_params['last_name'])
        self.assertEqual(mosteel.email, create_user_params['email'])

    def test_create_user_with_invalid_email(self):
        """
        Tests that creating a user with an invalid email causes
        status code 400 on the response and a validation error on the response JSON
        """
        response = self.create_post_request({
            'username': 'mosteel',
            'password': 'test',
            'first_name': 'Clark',
            'last_name': 'Kent',
            'email': 'someone',
        })

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.data['email'], [
            'Enter a valid email address.'
        ])

    def test_create_user_with_empty_password(self):
        """
        Tests that trying to create a user with an empty password fails
        with a 400 status code and an error message on the response.
        """
        response = self.create_post_request({
            'username': 'mosteel',
            'password': '',
            'first_name': 'Clark',
            'last_name': 'Kent',
            'email': 'clark@kent.com',
        })

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.data['password'], [
            'This field may not be blank.'
        ])

    def test_check_created_user_password(self):
        """
        Tests that once the user was created, it it assigned with the right
        password.
        """
        username = 'clark'
        password = 'kent'

        response = self.create_post_request({
            'username': username,
            'password': password,
            'first_name': 'Clark',
            'last_name': 'Kent',
            'email': 'clark@kent.com',
        })

        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username=username)
        check_password_result = user.check_password(password)

        self.assertEqual(check_password_result, True)
