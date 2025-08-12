import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationTestCase(APITestCase):
    """Test cases for organization functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.organization_data = {
            'name': 'Test Hospital',
            'email': 'test@hospital.com',
            'phone': '1234567890',
            'status': 'active',
            'address': {
                'street': '123 Test St',
                'city': 'Test City',
                'state': 'Test State',
                'pincode': '12345',
                'country': 'Test Country'
            }
        }
    
    def test_organization_serializer_valid(self):
        """Test organization serializer with valid data."""
        serializer = OrganizationSerializer(data=self.organization_data)
        self.assertTrue(serializer.is_valid())
    
    def test_organization_serializer_invalid(self):
        """Test organization serializer with invalid data."""
        invalid_data = {
            'name': '',
            'email': 'invalid-email',
            'phone': '123'
        }
        serializer = OrganizationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_create_organization(self):
        """Test creating an organization."""
        response = self.client.post('/api/v1/organizations/', 
                                  self.organization_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_organizations(self):
        """Test listing organizations."""
        response = self.client.get('/api/v1/organizations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 