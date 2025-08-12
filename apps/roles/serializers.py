from rest_framework import serializers
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""
    
    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description', 'permissions', 
            'is_active', 'is_deleted', 'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    
    def validate_name(self, value):
        """Validate role name uniqueness."""
        if Role.objects.filter(name=value, is_deleted=False).exists():
            raise serializers.ValidationError("A role with this name already exists.")
        return value
    
    def to_representation(self, instance):
        """Custom representation."""
        data = super().to_representation(instance)
        data['role_type'] = instance.name
        return data
