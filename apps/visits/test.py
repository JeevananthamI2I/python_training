import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Visit
from .serializers import VisitSerializer


class VisitTestCase(APITestCase):
    """Test cases for visit functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.visit_data = {
            'patient': 1,
            'doctor': 1,
            'technician': 1,
            'organization': 1,
            'scheduled_date': '2025-08-08T10:00:00Z',
            'status': 'scheduled',
            'priority': 'normal',
            'symptoms': 'Fever and cough',
            'diagnosis': 'Common cold',
            'prescription': 'Rest and fluids',
            'notes': 'Patient should rest for 3 days'
        }
    
    def test_visit_serializer_valid(self):
        """Test visit serializer with valid data."""
        serializer = VisitSerializer(data=self.visit_data)
        self.assertTrue(serializer.is_valid())
    
    def test_visit_serializer_invalid(self):
        """Test visit serializer with invalid data."""
        invalid_data = {
            'patient': None,
            'doctor': None,
            'organization': None,
            'scheduled_date': '2020-01-01T10:00:00Z'
        }
        serializer = VisitSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_create_visit(self):
        """Test creating a visit."""
        response = self.client.post('/api/v1/visits/', 
                                  self.visit_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_visits(self):
        """Test listing visits."""
        response = self.client.get('/api/v1/visits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 