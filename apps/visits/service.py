from .models import Visit
from .serializers import VisitSerializer


class VisitService:
    """Service class for visit operations."""
    
    @staticmethod
    def create_visit(data):
        """Create a new visit."""
        serializer = VisitSerializer(data=data)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def get_visit(visit_id):
        """Get visit by ID."""
        try:
            return Visit.objects.get(id=visit_id)
        except Visit.DoesNotExist:
            return None
    
    @staticmethod
    def list_visits():
        """List all visits."""
        return Visit.objects.all()
    
    @staticmethod
    def update_visit(visit, data):
        """Update visit."""
        serializer = VisitSerializer(visit, data=data, partial=True)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def delete_visit(visit):
        """Delete visit."""
        visit.delete()
        return True
    
    @staticmethod
    def get_patient_visits(patient_id):
        """Get visits for a specific patient."""
        return Visit.objects.filter(patient_id=patient_id)
    
    @staticmethod
    def get_doctor_visits(doctor_id):
        """Get visits for a specific doctor."""
        return Visit.objects.filter(doctor_id=doctor_id) 