from core.logging_config import get_logger
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from django.urls import NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, PermissionDenied, AuthenticationFailed

from .base import (
    CustomAPIException, ResourceNotFoundException, ValidationException,
    AuthenticationException, PermissionException, BusinessLogicException,
    DatabaseException, UserNotFoundException, OrganizationNotFoundException,
    PatientNotFoundException, VisitNotFoundException, RoleNotFoundException,
    AddressNotFoundException, InvalidCredentialsException, TokenExpiredException,
    InvalidTokenException, UserAlreadyExistsException, OrganizationAlreadyExistsException,
    PatientAlreadyExistsException
)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that provides detailed error messages.
    """
    # Get the request for trace_id
    request = context.get('request')
    trace_id = getattr(request, 'trace_id', 'unknown') if request else 'unknown'
    
    # Get logger
    logger = get_logger('django')
    
    # Handle Django's Http404
    if isinstance(exc, Http404):
        error_data = {
            'success': False,
            'error': 'Endpoint not found',
            'code': 'endpoint_not_found',
            'message': 'The requested API endpoint does not exist',
            'trace_id': trace_id,
            'details': {
                'path': request.path if request else 'unknown',
                'method': request.method if request else 'unknown'
            }
        }
        logger.warning(
            f"404 Error: {request.path} | Method: {request.method} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
        return Response(error_data, status=status.HTTP_404_NOT_FOUND)
    
    # Handle URL routing errors
    if isinstance(exc, NoReverseMatch):
        error_data = {
            'success': False,
            'error': 'URL routing error',
            'code': 'url_routing_error',
            'message': 'Invalid URL pattern or missing URL configuration',
            'trace_id': trace_id
        }
        logger.error(
            f"URL Routing Error: {exc} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
        return Response(error_data, status=status.HTTP_404_NOT_FOUND)
    
    # Handle DRF exceptions
    if isinstance(exc, NotFound):
        error_data = {
            'success': False,
            'error': 'Resource not found',
            'code': 'resource_not_found',
            'message': 'The requested resource does not exist',
            'trace_id': trace_id
        }
        logger.warning(
            f"Resource Not Found: {exc} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
        return Response(error_data, status=status.HTTP_404_NOT_FOUND)
    
    if isinstance(exc, PermissionDenied):
        error_data = {
            'success': False,
            'error': 'Permission denied',
            'code': 'permission_denied',
            'message': 'You do not have permission to perform this action',
            'trace_id': trace_id
        }
        logger.warning(
            f"Permission Denied: {exc} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
        return Response(error_data, status=status.HTTP_403_FORBIDDEN)
    
    if isinstance(exc, AuthenticationFailed):
        error_data = {
            'success': False,
            'error': 'Authentication failed',
            'code': 'authentication_failed',
            'message': 'Invalid authentication credentials',
            'trace_id': trace_id
        }
        logger.warning(
            f"Authentication Failed: {exc} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
        return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)
    
    # Handle Django database exceptions
    if isinstance(exc, ObjectDoesNotExist):
        error_data = {
            'success': False,
            'error': 'Object not found',
            'code': 'object_not_found',
            'message': 'The requested object does not exist in the database',
            'trace_id': trace_id
        }
        logger.warning(
            f"Object Not Found: {exc} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
        return Response(error_data, status=status.HTTP_404_NOT_FOUND)
    
    # Handle custom exceptions
    if isinstance(exc, CustomAPIException):
        error_data = {
            'success': False,
            'error': exc.message,
            'code': exc.code,
            'trace_id': trace_id
        }
        
        if hasattr(exc, 'details') and exc.details:
            error_data['details'] = exc.details
        
        logger.error(
            f"Custom API Exception: {exc.message} | Code: {exc.code} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
        return Response(error_data, status=exc.status_code)
    
    # Call REST framework's default exception handler
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the error response format
        error_data = {
            'success': False,
            'error': str(exc),
            'code': getattr(exc, 'code', 'unknown_error'),
            'trace_id': trace_id
        }
        
        # Add details if available
        if hasattr(exc, 'details'):
            error_data['details'] = exc.details
        
        response.data = error_data
        
        # Log the error
        logger.error(
            f"DRF API Error: {exc} | Trace ID: {trace_id} | Status: {response.status_code}",
            extra={'trace_id': trace_id}
        )
        
    else:
        # Handle Django exceptions
        if isinstance(exc, ValidationError):
            error_data = {
                'success': False,
                'error': 'Validation error',
                'code': 'validation_error',
                'message': 'Data validation failed',
                'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc),
                'trace_id': trace_id
            }
            response = Response(error_data, status=status.HTTP_400_BAD_REQUEST)
            
        elif isinstance(exc, IntegrityError):
            error_data = {
                'success': False,
                'error': 'Database integrity error',
                'code': 'database_integrity_error',
                'message': 'Database constraint violation',
                'trace_id': trace_id
            }
            response = Response(error_data, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            # Handle any other unhandled exceptions
            error_data = {
                'success': False,
                'error': 'Internal server error',
                'code': 'internal_server_error',
                'message': 'An unexpected error occurred',
                'trace_id': trace_id
            }
            response = Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Log the error
        logger.error(
            f"Unhandled Exception: {exc} | Trace ID: {trace_id}",
            extra={'trace_id': trace_id}
        )
    
    return response 