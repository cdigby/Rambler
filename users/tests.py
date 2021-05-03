from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import UserForm


#Basic user model tests
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='bob', email='bob@bob.com', password='bob')

    def test_user_saved(self):
        bob = User.objects.get(username='bob')
        self.assertEqual(bob.email, 'bob@bob.com')

    def test_user_authenticates(self):
        self.assertIsNotNone(authenticate(username='bob', password='bob'))

#Test validation with user form
class UserFormTestCase(TestCase):
    def test_create_valid_user(self):
        data = {
            'username': 'bob',
            'email': 'bob@bob.com',
            'password': 'bob',
            'password_confirmation': 'bob'
        }
        f = UserForm(data)
        self.assertTrue(f.is_valid())
        User.objects.create_user(username=f.cleaned_data['username'], email=f.cleaned_data['email'], password=f.cleaned_data['password'])
        bob = User.objects.get(username='bob')
        self.assertEqual(bob.email, 'bob@bob.com')
        self.assertIsNotNone(authenticate(username='bob', password='bob'))

    def test_create_other_valid_user(self):
        data = {
            'username': 'fred',
            'email': 'fred@fred.com',
            'password': 'fred',
            'password_confirmation': 'fred'
        }
        f = UserForm(data)
        self.assertTrue(f.is_valid())
        User.objects.create_user(username=f.cleaned_data['username'], email=f.cleaned_data['email'], password=f.cleaned_data['password'])
        bob = User.objects.get(username='fred')
        self.assertEqual(bob.email, 'fred@fred.com')
        self.assertIsNotNone(authenticate(username='fred', password='fred'))

    def test_invalid_email(self):
        data = {
            'username': 'harry',
            'email': 'h',
            'password': 'harry',
            'password_confirmation': 'harry'
        }
        f = UserForm(data)
        self.assertFalse(f.is_valid())

    def test_taken_username(self):
        data = {
            'username': 'bob',
            'email': 'bob@bob.com',
            'password': 'bob',
            'password_confirmation': 'bob'
        }
        f = UserForm(data)
        self.assertFalse(f.is_valid())

    def test_non_matching_passwords(self):
        data = {
            'username': 'george',
            'email': 'george@george.com',
            'password': 'george',
            'password_confirmation': 'boris'
        }
        f = UserForm(data)
        self.assertFalse(f.is_valid())