from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from datetime import date
from core.logging_config import get_logger

from .models import Visit
from .serializers import VisitSerializer
from core.utils.response import success_response, error_response


logger = get_logger('visits')


class VisitPagination(PageNumberPagination):
    """Custom pagination for Visit views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class VisitListView(APIView):
    """List all active visits with filtering and pagination."""
    permission_classes = [IsAuthenticated]
    pagination_class = VisitPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'organization', 'doctor', 'patient', 'scheduled_date']
    search_fields = ['symptoms', 'diagnosis', 'prescription', 'notes']
    ordering_fields = ['scheduled_date', 'actual_date', 'status', 'priority', 'created_at']
    ordering = ['-scheduled_date']
    
    def get(self, request):
        """List all active visits."""
        try:
            queryset = Visit.objects.filter(is_deleted=False)
            
            # Apply filters
            queryset = self.apply_filters(queryset, request)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = VisitSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = VisitSerializer(queryset, many=True)
            
            logger.info(f"Visits listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Visits retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing visits: {str(e)}")
            return error_response(
                error_message="Failed to retrieve visits",
                error_code="visit_list_error"
            )
    
    def apply_filters(self, queryset, request):
        """Apply filters to queryset."""
        # Status filter
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Priority filter
        priority_filter = request.query_params.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        # Organization filter
        org_filter = request.query_params.get('organization')
        if org_filter:
            queryset = queryset.filter(organization__name__icontains=org_filter)
        
        # Doctor filter
        doctor_filter = request.query_params.get('doctor')
        if doctor_filter:
            queryset = queryset.filter(doctor__email__icontains=doctor_filter)
        
        # Patient filter
        patient_filter = request.query_params.get('patient')
        if patient_filter:
            queryset = queryset.filter(patient__name__icontains=patient_filter)
        
        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                symptoms__icontains=search
            ) | queryset.filter(
                diagnosis__icontains=search
            ) | queryset.filter(
                prescription__icontains=search
            ) | queryset.filter(
                notes__icontains=search
            )
        
        # Ordering
        ordering = request.query_params.get('ordering', '-scheduled_date')
        if ordering in self.ordering_fields or ordering.lstrip('-') in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        
        return queryset


class VisitCreateView(APIView):
    """Create a new visit."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a new visit."""
        try:
            serializer = VisitSerializer(data=request.data)
            if serializer.is_valid():
                visit = serializer.save()
                
                logger.info(f"Visit created successfully: {visit.id}")
                return success_response(
                    data=serializer.data,
                    message="Visit created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"Visit creation failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid visit data",
                    error_code="visit_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error creating visit: {str(e)}")
            return error_response(
                error_message="Failed to create visit",
                error_code="visit_creation_error"
            )


class VisitDetailView(APIView):
    """Retrieve, update, and delete a specific visit."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Retrieve a specific visit."""
        try:
            visit = get_object_or_404(Visit, pk=pk, is_deleted=False)
            serializer = VisitSerializer(visit)
            
            logger.info(f"Visit retrieved successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Visit retrieved successfully"
            )
        except Visit.DoesNotExist:
            logger.warning(f"Visit not found: {pk}")
            return error_response(
                error_message="Visit not found",
                error_code="visit_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving visit: {str(e)}")
            return error_response(
                error_message="Failed to retrieve visit",
                error_code="visit_retrieval_error"
            )
    
    def put(self, request, pk):
        """Update a visit."""
        try:
            visit = get_object_or_404(Visit, pk=pk, is_deleted=False)
            serializer = VisitSerializer(visit, data=request.data, partial=True)
            
            if serializer.is_valid():
                visit = serializer.save()
                
                logger.info(f"Visit updated successfully: {pk}")
                return success_response(
                    data=serializer.data,
                    message="Visit updated successfully"
                )
            else:
                logger.warning(f"Visit update failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid visit data",
                    error_code="visit_validation_error",
                    details=serializer.errors
                )
        except Visit.DoesNotExist:
            logger.warning(f"Visit not found: {pk}")
            return error_response(
                error_message="Visit not found",
                error_code="visit_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating visit: {str(e)}")
            return error_response(
                error_message="Failed to update visit",
                error_code="visit_update_error"
            )
    
    def delete(self, request, pk):
        """Soft delete a visit."""
        try:
            visit = get_object_or_404(Visit, pk=pk, is_deleted=False)
            visit.soft_delete()
            
            logger.info(f"Visit soft deleted successfully: {pk}")
            return success_response(
                data={},
                message="Visit deleted successfully"
            )
        except Visit.DoesNotExist:
            logger.warning(f"Visit not found: {pk}")
            return error_response(
                error_message="Visit not found",
                error_code="visit_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting visit: {str(e)}")
            return error_response(
                error_message="Failed to delete visit",
                error_code="visit_deletion_error"
            )


class VisitRestoreView(APIView):
    """Restore a soft deleted visit."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Restore a soft deleted visit."""
        try:
            visit = get_object_or_404(Visit, pk=pk, is_deleted=True)
            visit.restore()
            
            serializer = VisitSerializer(visit)
            logger.info(f"Visit restored successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Visit restored successfully"
            )
        except Visit.DoesNotExist:
            logger.warning(f"Visit not found: {pk}")
            return error_response(
                error_message="Visit not found",
                error_code="visit_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error restoring visit: {str(e)}")
            return error_response(
                error_message="Failed to restore visit",
                error_code="visit_restore_error"
            )


class VisitCompleteView(APIView):
    """Complete a visit."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Complete a visit."""
        try:
            visit = get_object_or_404(Visit, pk=pk, is_deleted=False)
            
            if visit.status == 'completed':
                return error_response(
                    error_message="Visit is already completed",
                    error_code="visit_already_completed",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            visit.status = 'completed'
            visit.actual_date = timezone.now()
            visit.save()
            
            serializer = VisitSerializer(visit)
            logger.info(f"Visit completed successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Visit completed successfully"
            )
        except Visit.DoesNotExist:
            logger.warning(f"Visit not found: {pk}")
            return error_response(
                error_message="Visit not found",
                error_code="visit_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error completing visit: {str(e)}")
            return error_response(
                error_message="Failed to complete visit",
                error_code="visit_completion_error"
            )


class VisitCancelView(APIView):
    """Cancel a visit."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Cancel a visit."""
        try:
            visit = get_object_or_404(Visit, pk=pk, is_deleted=False)
            
            if visit.status == 'cancelled':
                return error_response(
                    error_message="Visit is already cancelled",
                    error_code="visit_already_cancelled",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            visit.status = 'cancelled'
            visit.save()
            
            serializer = VisitSerializer(visit)
            logger.info(f"Visit cancelled successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Visit cancelled successfully"
            )
        except Visit.DoesNotExist:
            logger.warning(f"Visit not found: {pk}")
            return error_response(
                error_message="Visit not found",
                error_code="visit_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error cancelling visit: {str(e)}")
            return error_response(
                error_message="Failed to cancel visit",
                error_code="visit_cancellation_error"
            )


class VisitDeletedListView(APIView):
    """List all soft deleted visits."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """List all soft deleted visits."""
        try:
            queryset = Visit.objects.filter(is_deleted=True)
            serializer = VisitSerializer(queryset, many=True)
            
            logger.info(f"Deleted visits listed. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Deleted visits retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing deleted visits: {str(e)}")
            return error_response(
                error_message="Failed to retrieve deleted visits",
                error_code="visit_deleted_list_error"
            )


class VisitUpcomingListView(APIView):
    """List upcoming visits."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """List upcoming visits."""
        try:
            today = timezone.now().date()
            queryset = Visit.objects.filter(
                is_deleted=False,
                scheduled_date__gte=today,
                status__in=['scheduled', 'confirmed']
            ).order_by('scheduled_date')
            
            serializer = VisitSerializer(queryset, many=True)
            
            logger.info(f"Upcoming visits listed. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Upcoming visits retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing upcoming visits: {str(e)}")
            return error_response(
                error_message="Failed to retrieve upcoming visits",
                error_code="visit_upcoming_list_error"
            )


class VisitTodayListView(APIView):
    """List today's visits."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """List today's visits."""
        try:
            today = timezone.now().date()
            queryset = Visit.objects.filter(
                is_deleted=False,
                scheduled_date__date=today
            ).order_by('scheduled_date')
            
            serializer = VisitSerializer(queryset, many=True)
            
            logger.info(f"Today's visits listed. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Today's visits retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing today's visits: {str(e)}")
            return error_response(
                error_message="Failed to retrieve today's visits",
                error_code="visit_today_list_error"
            )
