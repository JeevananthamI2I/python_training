from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from core.logging_config import get_logger

from .models import Organization
from .serializers import (
    OrganizationCreateSerializer, OrganizationSerializer, 
    OrganizationListSerializer, OrganizationDetailSerializer
)
from core.utils.response import success_response
from core.utils.error_utils import (
    safe_get_object_or_404, handle_integrity_error, 
    validate_required_fields, log_and_raise_exception
)
from core.exceptions.base import (
    OrganizationNotFoundException, OrganizationAlreadyExistsException,
    ValidationException, DatabaseException
)


logger = get_logger('organizations')


class OrganizationPagination(PageNumberPagination):
    """Custom pagination for Organization views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrganizationCreateView(APIView):
    """Create a new organization (HMS Flow Step 2)."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a new organization."""
        try:
            serializer = OrganizationCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                organization = serializer.save()
                
                # Prepare response data according to API documentation
                response_data = {
                    'organization_id': organization.id,
                    'organization': {
                        'id': organization.id,
                        'name': organization.name,
                        'type': organization.type,
                        'email': organization.email,
                        'phone': organization.phone,
                        'status': organization.status,
                        'address': {
                            'city': organization.address.city,
                            'state': organization.address.state,
                            'pincode': organization.address.pincode,
                            'country': organization.address.country
                        } if organization.address else None
                    }
                }
                
                logger.info(f"Organization created successfully: {organization.name}")
                return success_response(
                    data=response_data,
                    message="Organization created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"Organization creation failed: {serializer.errors}")
                return success_response(
                    data={},
                    message="Invalid organization data",
                    error_code="organization_creation_validation_error",
                    details=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error creating organization: {str(e)}")
            return success_response(
                data={},
                message="Failed to create organization",
                error_code="organization_creation_error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrganizationListView(APIView):
    """List all active organizations with filtering and pagination."""
    permission_classes = [IsAuthenticated]
    pagination_class = OrganizationPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at', 'status']
    ordering = ['-created_at']
    
    def get(self, request):
        """List all active organizations."""
        try:
            queryset = Organization.objects.filter(is_deleted=False)
            
            # Apply filters
            queryset = self.apply_filters(queryset, request)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = OrganizationListSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = OrganizationListSerializer(queryset, many=True)
            
            logger.info(f"Organizations listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Organizations retrieved successfully"
            )
        except Exception as e:
            log_and_raise_exception(logger, e, "Error listing organizations")
    
    def apply_filters(self, queryset, request):
        """Apply filters to queryset."""
        # Status filter
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                phone__icontains=search
            )
        
        # Ordering
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering in self.ordering_fields or ordering.lstrip('-') in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        
        return queryset


class OrganizationDetailView(APIView):
    """Retrieve, update, and delete a specific organization."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Retrieve organization details."""
        try:
            organization = get_object_or_404(Organization, id=pk, is_deleted=False)
            serializer = OrganizationDetailSerializer(organization)
            
            logger.info(f"Organization details retrieved: {organization.name}")
            return success_response(
                data=serializer.data,
                message="Organization details retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error retrieving organization details: {str(e)}")
            return success_response(
                data={},
                message="Failed to retrieve organization details",
                error_code="organization_detail_error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, pk):
        """Update organization."""
        try:
            organization = get_object_or_404(Organization, id=pk, is_deleted=False)
            serializer = OrganizationSerializer(organization, data=request.data, partial=True)
            
            if serializer.is_valid():
                organization = serializer.save()
                
                logger.info(f"Organization updated successfully: {organization.name}")
                return success_response(
                    data=OrganizationDetailSerializer(organization).data,
                    message="Organization updated successfully"
                )
            else:
                logger.warning(f"Organization update failed: {serializer.errors}")
                return success_response(
                    data={},
                    message="Invalid update data",
                    error_code="organization_update_validation_error",
                    details=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error updating organization: {str(e)}")
            return success_response(
                data={},
                message="Failed to update organization",
                error_code="organization_update_error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, pk):
        """Soft delete organization."""
        try:
            organization = get_object_or_404(Organization, id=pk, is_deleted=False)
            organization.soft_delete()
            
            logger.info(f"Organization soft deleted: {organization.name}")
            return success_response(
                data={},
                message="Organization deleted successfully"
            )
        except Exception as e:
            logger.error(f"Error deleting organization: {str(e)}")
            return success_response(
                data={},
                message="Failed to delete organization",
                error_code="organization_delete_error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrganizationRestoreView(APIView):
    """Restore a soft deleted organization."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Restore organization."""
        try:
            organization = get_object_or_404(Organization, id=pk, is_deleted=True)
            organization.restore()
            
            logger.info(f"Organization restored: {organization.name}")
            return success_response(
                data=OrganizationDetailSerializer(organization).data,
                message="Organization restored successfully"
            )
        except Exception as e:
            logger.error(f"Error restoring organization: {str(e)}")
            return success_response(
                data={},
                message="Failed to restore organization",
                error_code="organization_restore_error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrganizationStatusView(APIView):
    """Get organization status."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Get organization status."""
        try:
            organization = get_object_or_404(Organization, id=pk, is_deleted=False)
            
            status_data = {
                'id': organization.id,
                'name': organization.name,
                'status': organization.status,
                'is_active': organization.is_active,
                'created_at': organization.created_at,
                'updated_at': organization.updated_at
            }
            
            logger.info(f"Organization status retrieved: {organization.name}")
            return success_response(
                data=status_data,
                message="Organization status retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error retrieving organization status: {str(e)}")
            return success_response(
                data={},
                message="Failed to retrieve organization status",
                error_code="organization_status_error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrganizationDeletedListView(APIView):
    """List all soft deleted organizations."""
    permission_classes = [IsAuthenticated]
    pagination_class = OrganizationPagination
    
    def get(self, request):
        """List deleted organizations."""
        try:
            queryset = Organization.objects.filter(is_deleted=True)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = OrganizationListSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = OrganizationListSerializer(queryset, many=True)
            
            logger.info(f"Deleted organizations listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Deleted organizations retrieved successfully"
            )
        except Exception as e:
            log_and_raise_exception(logger, e, "Error listing deleted organizations")
