from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from core.logging_config import get_logger

from .models import Patient
from .serializers import PatientSerializer
from core.utils.response import success_response, error_response


logger = get_logger('patients')


class PatientPagination(PageNumberPagination):
    """Custom pagination for Patient views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PatientListView(APIView):
    """List all active patients with filtering and pagination."""
    permission_classes = [IsAuthenticated]
    pagination_class = PatientPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'gender', 'organization', 'blood_group', 'created_at']
    search_fields = ['name', 'email', 'phone', 'medical_history']
    ordering_fields = ['name', 'age', 'created_at', 'status']
    ordering = ['-created_at']
    
    def get(self, request):
        """List all active patients."""
        try:
            queryset = Patient.objects.filter(is_deleted=False)
            
            # Apply filters
            queryset = self.apply_filters(queryset, request)
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = PatientSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = PatientSerializer(queryset, many=True)
            
            logger.info(f"Patients listed successfully. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Patients retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing patients: {str(e)}")
            return error_response(
                error_message="Failed to retrieve patients",
                error_code="patient_list_error"
            )
    
    def apply_filters(self, queryset, request):
        """Apply filters to queryset."""
        # Status filter
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Gender filter
        gender_filter = request.query_params.get('gender')
        if gender_filter:
            queryset = queryset.filter(gender=gender_filter)
        
        # Organization filter
        org_filter = request.query_params.get('organization')
        if org_filter:
            queryset = queryset.filter(organization__name__icontains=org_filter)
        
        # Blood group filter
        blood_group_filter = request.query_params.get('blood_group')
        if blood_group_filter:
            queryset = queryset.filter(blood_group=blood_group_filter)
        
        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                phone__icontains=search
            ) | queryset.filter(
                medical_history__icontains=search
            )
        
        # Ordering
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering in self.ordering_fields or ordering.lstrip('-') in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        
        return queryset


class PatientCreateView(APIView):
    """Create a new patient."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a new patient."""
        try:
            serializer = PatientSerializer(data=request.data)
            if serializer.is_valid():
                patient = serializer.save()
                
                logger.info(f"Patient created successfully: {patient.id}", exc_info=True)
                return success_response(
                    data=serializer.data,
                    message="Patient created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            else:
                logger.warning(f"Patient creation failed: {serializer.errors}", exc_info=True)
                return error_response(
                    error_message="Invalid patient data",
                    error_code="patient_validation_error",
                    details=serializer.errors
                )
        except Exception as e:
            logger.error(f"Error creating patient: {str(e)}")
            return error_response(
                error_message="Failed to create patient",
                error_code="patient_creation_error"
            )


class PatientDetailView(APIView):
    """Retrieve, update, and delete a specific patient."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Retrieve a specific patient."""
        try:
            patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
            serializer = PatientSerializer(patient)
            
            logger.info(f"Patient retrieved successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Patient retrieved successfully"
            )
        except Patient.DoesNotExist:
            logger.warning(f"Patient not found: {pk}")
            return error_response(
                error_message="Patient not found",
                error_code="patient_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving patient: {str(e)}")
            return error_response(
                error_message="Failed to retrieve patient",
                error_code="patient_retrieval_error"
            )
    
    def put(self, request, pk):
        """Update a patient."""
        try:
            patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
            serializer = PatientSerializer(patient, data=request.data, partial=True)
            
            if serializer.is_valid():
                patient = serializer.save()
                
                logger.info(f"Patient updated successfully: {pk}")
                return success_response(
                    data=serializer.data,
                    message="Patient updated successfully"
                )
            else:
                logger.warning(f"Patient update failed: {serializer.errors}")
                return error_response(
                    error_message="Invalid patient data",
                    error_code="patient_validation_error",
                    details=serializer.errors
                )
        except Patient.DoesNotExist:
            logger.warning(f"Patient not found: {pk}")
            return error_response(
                error_message="Patient not found",
                error_code="patient_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating patient: {str(e)}")
            return error_response(
                error_message="Failed to update patient",
                error_code="patient_update_error"
            )
    
    def delete(self, request, pk):
        """Soft delete a patient."""
        try:
            patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
            patient.soft_delete()
            
            logger.info(f"Patient soft deleted successfully: {pk}")
            return success_response(
                data={},
                message="Patient deleted successfully"
            )
        except Patient.DoesNotExist:
            logger.warning(f"Patient not found: {pk}")
            return error_response(
                error_message="Patient not found",
                error_code="patient_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting patient: {str(e)}")
            return error_response(
                error_message="Failed to delete patient",
                error_code="patient_deletion_error"
            )


class PatientRestoreView(APIView):
    """Restore a soft deleted patient."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Restore a soft deleted patient."""
        try:
            patient = get_object_or_404(Patient, pk=pk, is_deleted=True)
            patient.restore()
            
            serializer = PatientSerializer(patient)
            logger.info(f"Patient restored successfully: {pk}")
            return success_response(
                data=serializer.data,
                message="Patient restored successfully"
            )
        except Patient.DoesNotExist:
            logger.warning(f"Patient not found: {pk}")
            return error_response(
                error_message="Patient not found",
                error_code="patient_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error restoring patient: {str(e)}")
            return error_response(
                error_message="Failed to restore patient",
                error_code="patient_restore_error"
            )


class PatientMedicalHistoryView(APIView):
    """Get patient medical history."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """Get patient medical history."""
        try:
            patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
            
            # Get medical history from visits
            from apps.visits.models import Visit
            visits = Visit.objects.filter(
                patient=patient,
                is_deleted=False,
                status='completed'
            ).order_by('-actual_date')
            
            medical_history = []
            for visit in visits:
                medical_history.append({
                    'visit_id': str(visit.id),
                    'date': visit.actual_date,
                    'symptoms': visit.symptoms,
                    'diagnosis': visit.diagnosis,
                    'prescription': visit.prescription,
                    'notes': visit.notes,
                    'doctor': visit.doctor.full_name if visit.doctor else None
                })
            
            logger.info(f"Patient medical history retrieved: {pk}")
            return success_response(
                data={'medical_history': medical_history},
                message="Patient medical history retrieved successfully"
            )
        except Patient.DoesNotExist:
            logger.warning(f"Patient not found: {pk}")
            return error_response(
                error_message="Patient not found",
                error_code="patient_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving patient medical history: {str(e)}")
            return error_response(
                error_message="Failed to retrieve patient medical history",
                error_code="patient_medical_history_error"
            )


class PatientDeletedListView(APIView):
    """List all soft deleted patients."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """List all soft deleted patients."""
        try:
            queryset = Patient.objects.filter(is_deleted=True)
            serializer = PatientSerializer(queryset, many=True)
            
            logger.info(f"Deleted patients listed. Count: {len(queryset)}")
            return success_response(
                data=serializer.data,
                message="Deleted patients retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing deleted patients: {str(e)}")
            return error_response(
                error_message="Failed to retrieve deleted patients",
                error_code="patient_deleted_list_error"
            )


class PatientBloodGroupsView(APIView):
    """Get list of all blood groups."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get list of all blood groups."""
        try:
            blood_groups = Patient.objects.filter(
                is_deleted=False
            ).values_list('blood_group', flat=True).distinct()
            
            logger.info(f"Blood groups listed. Count: {len(blood_groups)}")
            return success_response(
                data={'blood_groups': list(blood_groups)},
                message="Blood groups retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing blood groups: {str(e)}")
            return error_response(
                error_message="Failed to retrieve blood groups",
                error_code="blood_group_list_error"
            )
