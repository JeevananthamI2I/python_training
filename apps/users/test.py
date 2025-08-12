import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from .serializers import UserSerializer


class UserTestCase(APITestCase):
    """Test cases for user functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'status': 'active'
        }
    
    def test_user_serializer_valid(self):
        """Test user serializer with valid data."""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
    
    def test_user_serializer_invalid(self):
        """Test user serializer with invalid data."""
        invalid_data = {
            'email': 'invalid-email',
            'username': '',
            'password': '123',
            'password_confirm': '456'
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_create_user(self):
        """Test creating a user."""
        response = self.client.post('/api/v1/users/', 
                                  self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_users(self):
        """Test listing users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 