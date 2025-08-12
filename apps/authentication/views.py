from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.logging_config import get_logger

from apps.users.models import User
from apps.users.serializers import UserSerializer
from .serializers import LoginSerializer
from core.utils.response import success_response, error_response


logger = get_logger('authentication')


class UserRegistrationView(APIView):
    """Register a new user."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Register a new user."""
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"User registered successfully: {user.email}")
                return success_response(
                    data={
                        'user': serializer.data,
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        }
                    },
                    message="User registered successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"User registration failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid registration data",
                    error_code="registration_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")
            return error_response(
                error_message="Failed to register user",
                error_code="registration_error"
            )


class UserLoginView(APIView):
    """Login user and return tokens."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Login user and return tokens."""
        logger.info("Login method called")
        try:
            logger.info(f"Request data: {request.data}")
            
            # Validate input data
            serializer = LoginSerializer(data=request.data)
            logger.info("Serializer created")
            
            if not serializer.is_valid():
                logger.warning(f"Serializer validation failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid input data",
                    error_code="validation_error",
                    details=serializer.errors
                )
            
            logger.info("Serializer validation passed")
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            logger.info(f"Email: {email}")
            
            # Try to get user by email
            try:
                user = User.objects.get(email=email)
                logger.info("User found")
            except User.DoesNotExist:
                logger.warning(f"User not found for email: {email}")
                return error_response(
                    error_message="Invalid credentials",
                    error_code="invalid_credentials",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            
            # Check password
            if user.check_password(password):
                logger.info("Password is correct")
                refresh = RefreshToken.for_user(user)
                logger.info("JWT token generated")
                
                # Create simple user data
                user_data = {
                    'id': str(user.id),
                    'email': user.email,
                    'username': user.username,
                    'is_superuser': user.is_superuser,
                    'is_active': user.is_active
                }
                
                logger.info(f"User logged in successfully: {email}")
                return success_response(
                    data={
                        'user': user_data,
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        }
                    },
                    message="Login successful"
                )
            else:
                logger.warning(f"Invalid password for email: {email}")
                return error_response(
                    error_message="Invalid credentials",
                    error_code="invalid_credentials",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return error_response(
                error_message="Login failed",
                error_code="login_error"
            )
