from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from apps.addresses.serializers import AddressSerializer
from apps.roles.models import Role


class RoleCreateSerializer(serializers.Serializer):
    """For creating or updating Role during user operations."""
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer with nested address & role handling."""
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    address = AddressSerializer(required=False)
    role = RoleCreateSerializer(required=False)
    organization_id = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone',
            'gender', 'date_of_birth', 'organization', 'role', 'address',
            'status', 'password', 'password_confirm', 'organization_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization']
    
    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords don't match.")
        validate_password(data.get('password'))
        
        role_data = data.get('role')
        organization_id = data.get('organization_id')
        
        # Admin users can skip org validation only on first creation
        if role_data and role_data.get('name', '').lower() == 'admin' and not organization_id:
            pass
        elif not organization_id:
            raise serializers.ValidationError("organization_id is required for non-admin users.")
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm', None)
        address_data = validated_data.pop('address', None)
        role_data = validated_data.pop('role', None)
        organization_id = validated_data.pop('organization_id', None)
        
        # Generate username from email if missing
        if not validated_data.get('username'):
            email = validated_data.get('email')
            if email:
                base_username = email.split('@')[0]
                # Handle potential username conflicts
                username = base_username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}_{counter}"
                    counter += 1
                validated_data['username'] = username
            else:
                # Fallback username generation
                validated_data['username'] = f"user_{User.objects.count() + 1}"
        
        # Handle role creation or retrieval
        if role_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data.get('description', ''), 'is_active': True}
            )
            validated_data['role'] = role
        
        # Handle organization assignment
        if organization_id:
            from apps.organizations.models import Organization
            try:
                organization = Organization.objects.get(id=organization_id, is_deleted=False)
                validated_data['organization'] = organization
            except Organization.DoesNotExist:
                raise serializers.ValidationError("Invalid organization_id.")
        
        # Handle address creation
        if address_data:
            from apps.addresses.models import Address
            address = Address.objects.create(**address_data)
            validated_data['address'] = address
        
        # Ensure username is set
        if not validated_data.get('username'):
            raise serializers.ValidationError("Username generation failed")
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for updating User."""
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)
    address = AddressSerializer(required=False)
    role = RoleCreateSerializer(required=False)
    organization_id = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone',
            'gender', 'date_of_birth', 'organization', 'role', 'address',
            'status', 'password', 'password_confirm', 'organization_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization']
    
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError("Passwords don't match.")
        
        if password:
            validate_password(password)
        
        return data
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        address_data = validated_data.pop('address', None)
        role_data = validated_data.pop('role', None)
        organization_id = validated_data.pop('organization_id', None)
        
        # Update role if provided
        if role_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data.get('description', ''), 'is_active': True}
            )
            validated_data['role'] = role
        
        # Update organization if provided
        if organization_id:
            from apps.organizations.models import Organization
            try:
                organization = Organization.objects.get(id=organization_id, is_deleted=False)
                validated_data['organization'] = organization
            except Organization.DoesNotExist:
                raise serializers.ValidationError("Invalid organization_id.")
        
        # Update or create address
        if address_data:
            if instance.address:
                for attr, value in address_data.items():
                    setattr(instance.address, attr, value)
                instance.address.save()
            else:
                from apps.addresses.models import Address
                address = Address.objects.create(**address_data)
                validated_data['address'] = address
        
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """Simple list view serializer."""
    address = AddressSerializer(read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'phone', 'status',
            'role_name', 'organization_name', 'address'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user info serializer."""
    address = AddressSerializer(read_only=True)
    role = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'phone',
            'gender', 'date_of_birth', 'organization', 'role', 'address',
            'status', 'created_at', 'updated_at'
        ]
    
    def get_role(self, obj):
        if obj.role:
            return {
                'id': obj.role.id,
                'name': obj.role.name,
                'description': obj.role.description
            }
        return None
    
    def get_organization(self, obj):
        if obj.organization:
            return {
                'id': obj.organization.id,
                'name': obj.organization.name,
                'type': getattr(obj.organization, 'type', None)
            }
        return None
