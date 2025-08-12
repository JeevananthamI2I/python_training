import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer


class PatientTestCase(APITestCase):
    """Test cases for patient functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.patient_data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'male',
            'phone': '1234567890',
            'email': 'john@example.com',
            'blood_group': 'O+',
            'medical_history': 'No major issues',
            'allergies': 'None',
            'status': 'active',
            'address': {
                'street_address': '123 Test St',
                'city': 'Test City',
                'state': 'Test State',
                'pincode': '123456',
                'country': 'Test Country'
            }
        }
    
    def test_patient_serializer_valid(self):
        """Test patient serializer with valid data."""
        serializer = PatientSerializer(data=self.patient_data)
        self.assertTrue(serializer.is_valid())
    
    def test_patient_serializer_invalid(self):
        """Test patient serializer with invalid data."""
        invalid_data = {
            'name': '',
            'age': -5,
            'phone': '123'
        }
        serializer = PatientSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_create_patient(self):
        """Test creating a patient."""
        response = self.client.post('/api/v1/patients/', 
                                  self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_patients(self):
        """Test listing patients."""
        response = self.client.get('/api/v1/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 