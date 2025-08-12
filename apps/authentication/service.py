from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from .serializers import LoginSerializer


class AuthenticationService:
    """Service class for authentication operations."""
    
    @staticmethod
    def authenticate_user(email: str, password: str):
        """Authenticate user with email and password."""
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def generate_tokens(user):
        """Generate JWT tokens for user."""
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
    
    @staticmethod
    def validate_login_data(data):
        """Validate login data using serializer."""
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            return serializer.validated_data
        return None, serializer.errors 