from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model."""
    
    class Meta:
        model = Address
        fields = [
            'id', 'street_address', 'city', 'state', 'pincode', 'country'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_pincode(self, value):
        """Validate pincode format."""
        if value and len(value) < 6:
            raise serializers.ValidationError("Pincode must be at least 6 characters long.")
        return value
    
    def validate(self, data):
        """Validate address data."""
        if not data.get('city') or not data.get('state'):
            raise serializers.ValidationError("City and state are required.")
        return data 