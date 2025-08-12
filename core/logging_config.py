import logging
import logging.config
from django.conf import settings
import threading


class TraceIDFilter(logging.Filter):
    """Filter to automatically add trace ID to all log records."""
    
    def filter(self, record):
        # Try to get trace_id from the current request context
        try:
            current_thread = threading.current_thread()
            
            # Check if we're in a request context and have trace_id
            if hasattr(current_thread, '_request') and hasattr(current_thread._request, 'trace_id'):
                record.trace_id = current_thread._request.trace_id
            else:
                record.trace_id = 'no-trace-id'
        except Exception:
            record.trace_id = 'no-trace-id'
        
        return True


def setup_logging():
    """Setup logging configuration."""
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'trace_id': {
                '()': TraceIDFilter,
            },
        },
        'formatters': {
            'verbose': {
                'format': '[{asctime}] [{levelname}] [{name}]: {message}',
                'style': '{',
            },
            'verbose_with_trace': {
                'format': '[{asctime}] [trace_id={trace_id}] [{levelname}] [{name}]: {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose_with_trace',
                'filters': ['trace_id'],
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/meditrack360.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'verbose_with_trace',
                'filters': ['trace_id'],
                'encoding': 'utf-8',
            },
        },
        'root': {
            'handlers': ['console', 'file'],  # Use both console and file handlers
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'organizations': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'authentication': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'users': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'patients': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'visits': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'roles': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            'addresses': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    
    logging.config.dictConfig(logging_config)


def get_logger(name):
    """Get a logger instance."""
    return logging.getLogger(name) 