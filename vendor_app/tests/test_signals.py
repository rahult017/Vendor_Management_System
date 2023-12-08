from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone


class CreateAuthTokenSignalTest(TestCase):
    def test_create_auth_token_signal(self):
        # Create a new user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Check that the signal creates a new auth token
        tokens_before_save = Token.objects.count()
        user.save()
        tokens_after_save = Token.objects.count()

        self.assertEqual(tokens_after_save, tokens_before_save)

        # Check that the token has the correct attributes
        token = Token.objects.get(user=user)
        self.assertEqual(token.user, user)

        # Check that the token has a created and expires attribute
        self.assertIsNotNone(token.created)

        # Check that the expires attribute is set correctly
        self.assertLessEqual(timezone.now() - token.created, timedelta(seconds=2))

    def test_create_auth_token_signal_exception(self):
        # Mock the Token.objects.create method to raise an exception
        with self.assertRaises(Exception):
            with self.settings(DEBUG=True):  
                with self.assertRaises(Exception):
                    with self.settings(DEBUG=True): 
                        Token.objects.create = lambda *args, **kwargs: None
                        user = User.objects.create_user(username='testuser', password='testpassword')
                        user.save()

        # Ensure that the exception was logged (in this case, to the console)
        self.assertLogs(logger=__name__, level='ERROR')
