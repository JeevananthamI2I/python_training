from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Serializer for login requests."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """Validate login data."""
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        
        return data 