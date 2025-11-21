from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserRegistrationTest(TestCase):
    """ Test suite for user registration endpoint. """

    def setUp(self):
        self.client = APIClient()

    def test_user_registration_creates_profile(self):
        """Test that registering a new user creates a user profile."""
        # ARRANGE
        data = {
            'username': 'testuser',
            'password': 'TestPass123',
            'email': 'test@example.com',
            'name': 'Test User'
        }
        # ACT
        response = self.client.post('/register/', data, format='json') 
        # ASSERT
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify the user was created
        user = User.objects.filter(username='testuser').first()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.name, data['name'])
