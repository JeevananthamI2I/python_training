import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.authentication.serializers import LoginSerializer


class AuthenticationTestCase(APITestCase):
    """Test cases for authentication functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_serializer_valid(self):
        """Test login serializer with valid data."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_login_serializer_invalid(self):
        """Test login serializer with invalid data."""
        data = {
            'email': 'invalid-email',
            'password': ''
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_login_endpoint(self):
        """Test login endpoint."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/v1/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 