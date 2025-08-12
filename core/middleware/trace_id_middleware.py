import uuid
from django.utils.deprecation import MiddlewareMixin
import threading


class TraceIDMiddleware(MiddlewareMixin):
    """
    Middleware to add a unique trace ID to each request for logging purposes.
    """
    
    def process_request(self, request):
        """Generate a unique trace ID for the request."""
        trace_id = str(uuid.uuid4())
        request.trace_id = trace_id
        
        # Store request in current thread for logging access
        current_thread = threading.current_thread()
        current_thread._request = request
        
        return None
    
    def process_response(self, request, response):
        """Add trace ID to response headers for debugging."""
        if hasattr(request, 'trace_id'):
            response['X-Trace-ID'] = request.trace_id
        
        # Clean up thread storage
        current_thread = threading.current_thread()
        if hasattr(current_thread, '_request'):
            delattr(current_thread, '_request')
        
        return response
    
    def process_exception(self, request, exception):
        """Handle exceptions and clean up thread storage."""
        current_thread = threading.current_thread()
        if hasattr(current_thread, '_request'):
            delattr(current_thread, '_request')
        return None 