from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from core.logging_config import get_logger

from .models import Role
from .serializers import RoleSerializer
from core.utils.response import success_response, error_response


logger = get_logger('roles')


class RolePagination(PageNumberPagination):
    """Custom pagination for Role views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RoleListView(APIView):
    """List all active roles with filtering and pagination."""
    permission_classes = [IsAuthenticated]
    pagination_class = RolePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'is_active']
    ordering = ['name']
    
    def get(self, request):
        """List all active roles."""
        try:
            queryset = Role.objects.filter(is_deleted=False)
            
            # Apply filters
            queryset = self.apply_filters(queryset, request)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = RoleSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = RoleSerializer(queryset, many=True)
            
            logger.info(f"Roles listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Roles retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing roles: {str(e)}")
            return error_response(
                error_message="Failed to retrieve roles",
                error_code="role_list_error"
            )
    
    def apply_filters(self, queryset, request):
        """Apply filters to queryset."""
        # Active filter
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        # Ordering
        ordering = request.query_params.get('ordering', 'name')
        if ordering in self.ordering_fields or ordering.lstrip('-') in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        
        return queryset


class RoleCreateView(APIView):
    """Create a new role."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a new role."""
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                role = serializer.save()
                
                logger.info(f"Role created successfully: {role.id}")
                return success_response(
                    data=serializer.data,
                    message="Role created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"Role creation failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid role data",
                    error_code="role_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error creating role: {str(e)}")
            return error_response(
                error_message="Failed to create role",
                error_code="role_creation_error"
            )


class RoleDetailView(APIView):
    """Retrieve, update, and delete a specific role."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Retrieve a specific role."""
        try:
            role = get_object_or_404(Role, pk=pk, is_deleted=False)
            serializer = RoleSerializer(role)
            
            logger.info(f"Role retrieved successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Role retrieved successfully"
            )
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            return error_response(
                error_message="Role not found",
                error_code="role_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving role: {str(e)}")
            return error_response(
                error_message="Failed to retrieve role",
                error_code="role_retrieval_error"
            )
    
    def put(self, request, pk):
        """Update a role."""
        try:
            role = get_object_or_404(Role, pk=pk, is_deleted=False)
            serializer = RoleSerializer(role, data=request.data, partial=True)
            
            if serializer.is_valid():
                role = serializer.save()
                
                logger.info(f"Role updated successfully: {pk}")
                return success_response(
                    data=serializer.data,
                    message="Role updated successfully"
                )
            else:
                logger.warning(f"Role update failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid role data",
                    error_code="role_validation_error",
                    details=serializer.errors
                )
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            return error_response(
                error_message="Role not found",
                error_code="role_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating role: {str(e)}")
            return error_response(
                error_message="Failed to update role",
                error_code="role_update_error"
            )
    
    def delete(self, request, pk):
        """Soft delete a role."""
        try:
            role = get_object_or_404(Role, pk=pk, is_deleted=False)
            role.soft_delete()
            
            logger.info(f"Role soft deleted successfully: {pk}")
            return success_response(
                data={},
                message="Role deleted successfully"
            )
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            return error_response(
                error_message="Role not found",
                error_code="role_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting role: {str(e)}")
            return error_response(
                error_message="Failed to delete role",
                error_code="role_deletion_error"
            )


class RoleRestoreView(APIView):
    """Restore a soft deleted role."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Restore a soft deleted role."""
        try:
            role = get_object_or_404(Role, pk=pk, is_deleted=True)
            role.restore()
            
            serializer = RoleSerializer(role)
            logger.info(f"Role restored successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Role restored successfully"
            )
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            return error_response(
                error_message="Role not found",
                error_code="role_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error restoring role: {str(e)}")
            return error_response(
                error_message="Failed to restore role",
                error_code="role_restore_error"
            )


class RoleToggleStatusView(APIView):
    """Toggle role active status."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Toggle role active status."""
        try:
            role = get_object_or_404(Role, pk=pk, is_deleted=False)
            role.is_active = not role.is_active
            role.save()
            
            serializer = RoleSerializer(role)
            logger.info(f"Role status toggled successfully: {pk}")
            return success_response(
                data=serializer.data,
                message=f"Role {'activated' if role.is_active else 'deactivated'} successfully"
            )
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            return error_response(
                error_message="Role not found",
                error_code="role_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error toggling role status: {str(e)}")
            return error_response(
                error_message="Failed to toggle role status",
                error_code="role_status_toggle_error"
            )


class RoleDeletedListView(APIView):
    """List all soft deleted roles."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """List all soft deleted roles."""
        try:
            queryset = Role.objects.filter(is_deleted=True)
            serializer = RoleSerializer(queryset, many=True)
            
            logger.info(f"Deleted roles listed. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Deleted roles retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing deleted roles: {str(e)}")
            return error_response(
                error_message="Failed to retrieve deleted roles",
                error_code="role_deleted_list_error"
            )
