from .models import Address
from .serializers import AddressSerializer


class AddressService:
    """Service class for address operations."""
    
    @staticmethod
    def create_address(data):
        """Create a new address."""
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def get_address(address_id):
        """Get address by ID."""
        try:
            return Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return None
    
    @staticmethod
    def list_addresses():
        """List all addresses."""
        return Address.objects.all()
    
    @staticmethod
    def update_address(address, data):
        """Update address."""
        serializer = AddressSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            return serializer.save()
        return None, serializer.errors
    
    @staticmethod
    def delete_address(address):
        """Delete address."""
        address.delete()
        return True 