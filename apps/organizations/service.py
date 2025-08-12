from .models import Organization
from .serializers import OrganizationSerializer
from apps.addresses.models import Address


class OrganizationService:
    """Service class for organization operations."""
    
    @staticmethod
    def create_organization(data):
        """Create a new organization with address."""
        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def get_organization(org_id):
        """Get organization by ID."""
        try:
            return Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return None
    
    @staticmethod
    def list_organizations():
        """List all organizations."""
        return Organization.objects.all()
    
    @staticmethod
    def update_organization(organization, data):
        """Update organization."""
        serializer = OrganizationSerializer(organization, data=data, partial=True)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def delete_organization(organization):
        """Delete organization."""
        organization.delete()
        return True 