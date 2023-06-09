from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import User
from rest_framework.serializers import ValidationError
from django.test import TestCase
from .serializer import SignupSerializer, LoginSerializer, USerProfileSearchSerializer
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
class SignupViewTestCase(APITestCase):
    def test_valid_signup(self):
        """
        Test valid signup request.
        """
        url = reverse('sign_up')  # Replace 'signup' with your actual URL name
        data = {
            'email': 'test@example.com',
            'password': 'test123',
            'full_name': 'John Doe',
            'username': 'johndoe'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert that the user is created in the database
        self.assertTrue(User.objects.filter(email=data['email']).exists())

    def test_invalid_signup(self):
        """
        Test invalid signup request.
        """
        url = reverse('sign_up')  # Replace 'signup' with your actual URL name
        data = {
            'email': 'invalid_email',
            'password': '',
            'full_name': 'John Doe',
            'username': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that the response contains the expected error messages
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)
        self.assertIn('username', response.data)


class SignupSerializerTestCase(TestCase):
    def test_create_user(self):
        """
        Test creating a new user.
        """
        User = get_user_model()
        serializer = SignupSerializer()
        validated_data = {
            'email': 'test@example.com',
            'password': 'test123',
            'full_name': 'John Doe',
            'username': 'johndoe'
        }
        user = serializer.create(validated_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, validated_data['email'])
        self.assertEqual(user.full_name, validated_data['full_name'])
        self.assertEqual(user.username, validated_data['username'])
        self.assertTrue(user.check_password(validated_data['password']))

    def test_invalid_data(self):
        """
        Test serializer with invalid data.
        """
        # serializer = SignupSerializer()
        invalid_data = {
            'email': 'invalid_email',
            'password': '',
            'full_name': 'John Doe',
            'username': ''
        }
        with self.assertRaises(ValidationError):
            SignupSerializer(data=invalid_data).is_valid(raise_exception=True)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login_view')

    def test_login_valid_credentials(self):
        """
        Test login with valid credentials.
        """
        # Create a test user
        email = 'test@example.com'
        password = 'test123'
        user = User.objects.create_user(email=email, password=password)

        # Send login request with valid credentials
        data = {'email': email, 'password': password}
        response = self.client.post(self.url, data)

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        # Send login request with invalid credentials
        data = {'email': 'invalid_email', 'password': 'invalid_password'}
        response = self.client.post(self.url, data)

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Invalid email or password'])

class LoginSerializerTestCase(TestCase):
    def test_validate_with_valid_credentials(self):
        """
        Test serializer validation with valid credentials.
        """
        # Create a test user
        email = 'test@example.com'
        password = 'test123'
        user = User.objects.create_user(email=email, password=password)

        # Create serializer instance
        serializer = LoginSerializer(data={'email': email, 'password': password})
        serializer.is_valid(raise_exception=True)

        # Assert validated user
        validated_user = serializer.validated_data
        self.assertEqual(validated_user, user)

    def test_validate_with_invalid_credentials(self):
        """
        Test serializer validation with invalid credentials.
        """
        # Create serializer instance with invalid credentials
        serializer = LoginSerializer(data={'email': 'invalid_email', 'password': 'invalid_password'})

        # Assert validation error
        with self.assertRaises(serializers.ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        error_message = str(context.exception)
        self.assertIn('Invalid email or password', error_message)

# class SearchAllProfilesTestCase(APITestCase):
#     def setUp(self):
#         self.url = reverse('search_profile', args=['search_term'])
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    
#     def test_search_profiles(self):
#         """
#         Test searching profiles with a search term.
#         """
#         # Create some test users
#         user1 = User.objects.create_user(username='user1', email='user1@example.com', password='test123')
#         user2 = User.objects.create_user(username='user2', email='user2@example.com', password='test456')

#         self.client.force_authenticate(user=self.user)
#         # Perform search with a search term
#         search_term = 'user'
#         response = self.client.get(self.url.replace('search_term', search_term))

#         # Assert response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         serializer = USerProfileSearchSerializer([user1, user2], many=True)
#         expected_data = {'search_profiles': serializer.data}
#         self.assertEqual(response.data, expected_data)

#     def test_search_profiles_no_results(self):
#         """
#         Test searching profiles with no results.
#         """
#         # Perform search with a search term that doesn't match any profiles
#         self.client.force_authenticate(user=self.user)

#         # Perform search with a search term that doesn't match any profiles
#         search_term = 'xyz'
#         response = self.client.get(self.url.replace('search_term', search_term))

#         # Assert response
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(response.data, {'search_profiles': []})