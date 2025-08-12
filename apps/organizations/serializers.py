from rest_framework import serializers
from .models import Organization
from apps.addresses.serializers import AddressSerializer


class OrganizationCreateSerializer(serializers.ModelSerializer):
    """Serializer for Organization creation (HMS Flow Step 2)."""
    
    address = AddressSerializer()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'email', 'phone', 'status', 'address', 'type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create organization with nested address and link admin."""
        address_data = validated_data.pop('address', None)
        request = self.context.get('request')
        
        if address_data:
            from apps.addresses.models import Address
            address = Address.objects.create(**address_data)
            validated_data['address'] = address
        
        # Create the organization
        organization = Organization.objects.create(**validated_data)
        
        # Link the creating admin to the organization if they don't have one
        if request and request.user.is_authenticated:
            user = request.user
            if user.role and user.role.name.lower() == 'admin' and not user.organization:
                user.organization = organization
                user.save()
        
        return organization


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model updates and details."""
    
    address = AddressSerializer()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'email', 'phone', 'status', 'address', 'type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        """Update organization with nested address."""
        address_data = validated_data.pop('address', None)
        
        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class OrganizationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for organization list."""
    
    address = AddressSerializer()
    
    class Meta:
        model = Organization
        fields = ['id', 'name', 'email', 'status', 'address', 'type']


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for organization information."""
    
    address = AddressSerializer()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'email', 'phone', 'status', 'address', 'type',
            'created_at', 'updated_at'
        ] 