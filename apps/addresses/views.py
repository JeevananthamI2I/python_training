from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from core.logging_config import get_logger

from .models import Address
from .serializers import AddressSerializer
from core.utils.response import success_response, error_response


logger = get_logger('addresses')


class AddressPagination(PageNumberPagination):
    """Custom pagination for Address views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AddressListView(APIView):
    """List all active addresses with filtering and pagination."""
    permission_classes = [IsAuthenticated]
    pagination_class = AddressPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'state', 'country', 'created_at']
    search_fields = ['street_address', 'city', 'state', 'pincode', 'country']
    ordering_fields = ['city', 'state', 'created_at']
    ordering = ['-created_at']
    
    def get(self, request):
        """List all active addresses."""
        try:
            queryset = Address.objects.filter(is_deleted=False)
            
            # Apply filters
            queryset = self.apply_filters(queryset, request)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = AddressSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = AddressSerializer(queryset, many=True)
            
            logger.info(f"Addresses listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Addresses retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing addresses: {str(e)}")
            return error_response(
                error_message="Failed to retrieve addresses",
                error_code="address_list_error"
            )
    
    def apply_filters(self, queryset, request):
        """Apply filters to queryset."""
        # City filter
        city_filter = request.query_params.get('city')
        if city_filter:
            queryset = queryset.filter(city__icontains=city_filter)
        
        # State filter
        state_filter = request.query_params.get('state')
        if state_filter:
            queryset = queryset.filter(state__icontains=state_filter)
        
        # Country filter
        country_filter = request.query_params.get('country')
        if country_filter:
            queryset = queryset.filter(country__icontains=country_filter)
        
        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                street_address__icontains=search
            ) | queryset.filter(
                city__icontains=search
            ) | queryset.filter(
                state__icontains=search
            ) | queryset.filter(
                pincode__icontains=search
            ) | queryset.filter(
                country__icontains=search
            )
        
        # Ordering
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering in self.ordering_fields or ordering.lstrip('-') in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        
        return queryset


class AddressCreateView(APIView):
    """Create a new address."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a new address."""
        try:
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                address = serializer.save()
                
                logger.info(f"Address created successfully: {address.id}")
                return success_response(
                    data=serializer.data,
                    message="Address created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"Address creation failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid address data",
                    error_code="address_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error creating address: {str(e)}")
            return error_response(
                error_message="Failed to create address",
                error_code="address_creation_error"
            )


class AddressDetailView(APIView):
    """Retrieve, update, and delete a specific address."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Retrieve a specific address."""
        try:
            address = get_object_or_404(Address, pk=pk, is_deleted=False)
            serializer = AddressSerializer(address)
            
            logger.info(f"Address retrieved successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Address retrieved successfully"
            )
        except Address.DoesNotExist:
            logger.warning(f"Address not found: {pk}")
            return error_response(
                error_message="Address not found",
                error_code="address_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving address: {str(e)}")
            return error_response(
                error_message="Failed to retrieve address",
                error_code="address_retrieval_error"
            )
    
    def put(self, request, pk):
        """Update an address."""
        try:
            address = get_object_or_404(Address, pk=pk, is_deleted=False)
            serializer = AddressSerializer(address, data=request.data, partial=True)
            
            if serializer.is_valid():
                address = serializer.save()
                
                logger.info(f"Address updated successfully: {pk}")
                return success_response(
                    data=serializer.data,
                    message="Address updated successfully"
                )
            else:
                logger.warning(f"Address update failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid address data",
                    error_code="address_validation_error",
                    details=serializer.errors
                )
        except Address.DoesNotExist:
            logger.warning(f"Address not found: {pk}")
            return error_response(
                error_message="Address not found",
                error_code="address_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating address: {str(e)}")
            return error_response(
                error_message="Failed to update address",
                error_code="address_update_error"
            )
    
    def delete(self, request, pk):
        """Soft delete an address."""
        try:
            address = get_object_or_404(Address, pk=pk, is_deleted=False)
            address.soft_delete()
            
            logger.info(f"Address soft deleted successfully: {pk}")
            return success_response(
                data={},
                message="Address deleted successfully"
            )
        except Address.DoesNotExist:
            logger.warning(f"Address not found: {pk}")
            return error_response(
                error_message="Address not found",
                error_code="address_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting address: {str(e)}")
            return error_response(
                error_message="Failed to delete address",
                error_code="address_deletion_error"
            )


class AddressRestoreView(APIView):
    """Restore a soft deleted address."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Restore a soft deleted address."""
        try:
            address = get_object_or_404(Address, pk=pk, is_deleted=True)
            address.restore()
            
            serializer = AddressSerializer(address)
            logger.info(f"Address restored successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Address restored successfully"
            )
        except Address.DoesNotExist:
            logger.warning(f"Address not found: {pk}")
            return error_response(
                error_message="Address not found",
                error_code="address_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error restoring address: {str(e)}")
            return error_response(
                error_message="Failed to restore address",
                error_code="address_restore_error"
            )


class AddressDeletedListView(APIView):
    """List all soft deleted addresses."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """List all soft deleted addresses."""
        try:
            queryset = Address.objects.filter(is_deleted=True)
            serializer = AddressSerializer(queryset, many=True)
            
            logger.info(f"Deleted addresses listed. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Deleted addresses retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing deleted addresses: {str(e)}")
            return error_response(
                error_message="Failed to retrieve deleted addresses",
                error_code="address_deleted_list_error"
            )


class AddressCitiesView(APIView):
    """Get list of all cities."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get list of all cities."""
        try:
            cities = Address.objects.filter(
                is_deleted=False
            ).values_list('city', flat=True).distinct()
            
            logger.info(f"Cities listed. Count: {len(cities)}")
            return success_response(
                data={'cities': list(cities)},
                message="Cities retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing cities: {str(e)}")
            return error_response(
                error_message="Failed to retrieve cities",
                error_code="city_list_error"
            )


class AddressStatesView(APIView):
    """Get list of all states."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get list of all states."""
        try:
            states = Address.objects.filter(
                is_deleted=False
            ).values_list('state', flat=True).distinct()
            
            logger.info(f"States listed. Count: {len(states)}")
            return success_response(
                data={'states': list(states)},
                message="States retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing states: {str(e)}")
            return error_response(
                error_message="Failed to retrieve states",
                error_code="state_list_error"
            )
