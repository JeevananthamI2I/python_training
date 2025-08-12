from .models import Patient
from .serializers import PatientSerializer
from apps.addresses.models import Address


class PatientService:
    """Service class for patient operations."""
    
    @staticmethod
    def create_patient(data):
        """Create a new patient with address."""
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def get_patient(patient_id):
        """Get patient by ID."""
        try:
            return Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return None
    
    @staticmethod
    def list_patients():
        """List all patients."""
        return Patient.objects.all()
    
    @staticmethod
    def update_patient(patient, data):
        """Update patient."""
        serializer = PatientSerializer(patient, data=data, partial=True)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def delete_patient(patient):
        """Delete patient."""
        patient.delete()
        return True 