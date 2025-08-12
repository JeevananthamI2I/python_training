from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Response: Standardized success response
    """
    response_data = {
        'success': True,
        'message': message,
    }
    
    if data is not None:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)


def error_response(error_message, error_code=None, status_code=status.HTTP_400_BAD_REQUEST, details=None):
    """
    Create a standardized error response.
    
    Args:
        error_message: Error message
        error_code: Error code for client handling
        status_code: HTTP status code
        details: Additional error details
        
    Returns:
        Response: Standardized error response
    """
    response_data = {
        'success': False,
        'error': error_message,
    }
    
    if error_code:
        response_data['code'] = error_code
    
    if details:
        response_data['details'] = details
    
    return Response(response_data, status=status_code)


def paginated_response(data, count, next_url=None, previous_url=None, status_code=status.HTTP_200_OK):
    """
    Create a standardized paginated response.
    
    Args:
        data: Response data
        count: Total count of items
        next_url: URL for next page
        previous_url: URL for previous page
        status_code: HTTP status code
        
    Returns:
        Response: Standardized paginated response
    """
    response_data = {
        'success': True,
        'data': data,
        'pagination': {
            'count': count,
            'next': next_url,
            'previous': previous_url
        }
    }
    
    return Response(response_data, status=status_code) 