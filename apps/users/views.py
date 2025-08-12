from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from core.logging_config import get_logger

from .models import User
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserListSerializer, UserDetailSerializer
)
from core.utils.response import success_response, error_response


logger = get_logger('users')


class UserPagination(PageNumberPagination):
    """Custom pagination for User views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserRegistrationView(APIView):
    """User registration endpoint (HMS Flow Step 1 & 3)."""
    permission_classes = [AllowAny]  # Allow registration without authentication
    
    def post(self, request):
        """Register a new user."""
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Prepare response data according to API documentation
                response_data = {
                    'user_id': user.id,
                    'organization_id': user.organization.id if user.organization else None,
                    'role_id': user.role.id if user.role else None,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'phone': user.phone,
                        'status': user.status,
                        'role': {
                            'id': user.role.id,
                            'name': user.role.name,
                            'description': user.role.description
                        } if user.role else None,
                        'organization': {
                            'id': user.organization.id,
                            'name': user.organization.name
                        } if user.organization else None,
                        'address': {
                            'city': user.address.city,
                            'state': user.address.state,
                            'pincode': user.address.pincode,
                            'country': user.address.country
                        } if user.address else None
                    }
                }
                
                logger.info(f"User registered successfully: {user.email}")
                return success_response(
                    data=response_data,
                    message="User created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"User registration failed: {serializer.errors}", exc_info=True)
                return error_response(
                    error_message="Invalid user data",
                    error_code="user_creation_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to create user",
                error_code="user_creation_error"
            )


class UserListView(APIView):
    """List all active users with filtering and pagination."""
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'organization', 'role', 'gender', 'created_at']
    search_fields = ['email', 'username', 'phone']
    ordering_fields = ['email', 'username', 'created_at', 'status']
    ordering = ['-created_at']
    
    def get(self, request):
        """List all active users."""
        try:
            queryset = User.objects.filter(is_deleted=False)
            
            # Apply filters
            queryset = self.apply_filters(queryset, request)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = UserListSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = UserListSerializer(queryset, many=True)
            
            logger.info(f"Users listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Users retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to retrieve users",
                error_code="user_list_error"
            )
    
    def apply_filters(self, queryset, request):
        """Apply filters to queryset."""
        # Status filter
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Organization filter
        org_filter = request.query_params.get('organization')
        if org_filter:
            queryset = queryset.filter(organization__name__icontains=org_filter)
        
        # Role filter
        role_filter = request.query_params.get('role')
        if role_filter:
            queryset = queryset.filter(role__name__icontains=role_filter)
        
        # Gender filter
        gender_filter = request.query_params.get('gender')
        if gender_filter:
            queryset = queryset.filter(gender=gender_filter)
        
        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                phone__icontains=search
            )
        
        # Ordering
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering in self.ordering_fields or ordering.lstrip('-') in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        
        return queryset


class UserCreateView(APIView):
    """Create a new user with authentication."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a new user."""
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Prepare response data
                response_data = {
                    'user_id': user.id,
                    'organization_id': user.organization.id if user.organization else None,
                    'role_id': user.role.id if user.role else None,
                    'user': UserDetailSerializer(user).data
                }
                
                logger.info(f"User created successfully: {user.email}")
                return success_response(
                    data=response_data,
                    message="User created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"User creation failed: {serializer.errors}", exc_info=True)
                return error_response(
                    error_message="Invalid user data",
                    error_code="user_creation_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to create user",
                error_code="user_creation_error"
            )


class UserDetailView(APIView):
    """Retrieve, update, and delete a specific user."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Retrieve user details."""
        try:
            user = get_object_or_404(User, id=pk, is_deleted=False)
            serializer = UserDetailSerializer(user)
            
            logger.info(f"User details retrieved: {user.email}")
            return success_response(
                data=serializer.data,
                message="User details retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error retrieving user details: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to retrieve user details",
                error_code="user_detail_error"
            )
    
    def put(self, request, pk):
        """Update user."""
        try:
            user = get_object_or_404(User, id=pk, is_deleted=False)
            serializer = UserSerializer(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                user = serializer.save()
                
                logger.info(f"User updated successfully: {user.email}")
                return success_response(
                    data=UserDetailSerializer(user).data,
                    message="User updated successfully"
                )
            else:
                logger.warning(f"User update failed: {serializer.errors}", exc_info=True)
                return error_response(
                    error_message="Invalid update data",
                    error_code="user_update_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to update user",
                error_code="user_update_error"
            )
    
    def delete(self, request, pk):
        """Soft delete user."""
        try:
            user = get_object_or_404(User, id=pk, is_deleted=False)
            user.soft_delete()
            
            logger.info(f"User soft deleted: {user.email}")
            return success_response(
                data={},
                message="User deleted successfully"
            )
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to delete user",
                error_code="user_delete_error"
            )


class UserRestoreView(APIView):
    """Restore a soft deleted user."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Restore user."""
        try:
            user = get_object_or_404(User, id=pk, is_deleted=True)
            user.restore()
            
            logger.info(f"User restored: {user.email}")
            return success_response(
                data=UserDetailSerializer(user).data,
                message="User restored successfully"
            )
        except Exception as e:
            logger.error(f"Error restoring user: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to restore user",
                error_code="user_restore_error"
            )


class UserChangePasswordView(APIView):
    """Change user password."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Change user password."""
        try:
            user = get_object_or_404(User, id=pk, is_deleted=False)
            
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            
            if not old_password or not new_password:
                return error_response(
                    error_message="Both old_password and new_password are required",
                    error_code="password_change_validation_error"
                )
            
            if not user.check_password(old_password):
                return error_response(
                    error_message="Invalid old password",
                    error_code="invalid_old_password"
                )
            
            user.set_password(new_password)
            user.save()
            
            logger.info(f"User password changed: {user.email}")
            return success_response(
                data={},
                message="Password changed successfully"
            )
        except Exception as e:
            logger.error(f"Error changing user password: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to change password",
                error_code="password_change_error"
            )


class UserDeletedListView(APIView):
    """List all soft deleted users."""
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination
    
    def get(self, request):
        """List deleted users."""
        try:
            queryset = User.objects.filter(is_deleted=True)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = UserListSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = UserListSerializer(queryset, many=True)
            
            logger.info(f"Deleted users listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Deleted users retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing deleted users: {str(e)}", exc_info=True)
            return error_response(
                error_message="Failed to retrieve deleted users",
                error_code="user_deleted_list_error"
            )
