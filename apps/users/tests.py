from django.core.urlresolvers import resolve
from django.test import TestCase

from rest_framework.authtoken.views import obtain_auth_token


class UsersURLsTestCase(TestCase):
    def test_get_token_url_uses_obtain_token_view(self):
        """
        Test that the get token url resolves to the correct
        view function.
        """
        get_token = resolve('/api/v1/users/get-token/')
        self.assertEqual(get_token.func, obtain_auth_token)
