from rest_framework import serializers
from .models import Patient
from apps.addresses.serializers import AddressSerializer


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""
    
    address = AddressSerializer(required=False)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'age', 'gender', 'phone', 'email', 'date_of_birth',
            'blood_group', 'medical_history', 'allergies', 'organization',
            'created_by', 'address', 'status'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_age(self, value):
        """Validate age."""
        if value and (value < 0 or value > 150):
            raise serializers.ValidationError("Age must be between 0 and 150.")
        return value
    
    def validate_phone(self, value):
        """Validate phone number."""
        if value and len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value
    
    def create(self, validated_data):
        """Create patient with nested address."""
        address_data = validated_data.pop('address', None)
        
        if address_data:
            from apps.addresses.models import Address
            address = Address.objects.create(**address_data)
            validated_data['address'] = address
        
        return Patient.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update patient with nested address."""
        address_data = validated_data.pop('address', None)
        
        if address_data:
            if instance.address:
                address = instance.address
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                from apps.addresses.models import Address
                address = Address.objects.create(**address_data)
                validated_data['address'] = address
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance 