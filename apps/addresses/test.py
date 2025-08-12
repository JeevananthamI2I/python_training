import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Address
from .serializers import AddressSerializer


class AddressTestCase(APITestCase):
    """Test cases for address functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.address_data = {
            'street_address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'pincode': '123456',
            'country': 'Test Country'
        }
    
    def test_address_serializer_valid(self):
        """Test address serializer with valid data."""
        serializer = AddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
    
    def test_address_serializer_invalid(self):
        """Test address serializer with invalid data."""
        invalid_data = {
            'street_address': '123 Test St',
            'city': '',
            'state': '',
            'pincode': '123'
        }
        serializer = AddressSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_create_address(self):
        """Test creating an address."""
        response = self.client.post('/api/v1/addresses/', 
                                  self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_addresses(self):
        """Test listing addresses."""
        response = self.client.get('/api/v1/addresses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 