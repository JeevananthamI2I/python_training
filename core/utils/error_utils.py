from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from core.exceptions.base import (
    ResourceNotFoundException, ValidationException, BusinessLogicException,
    DatabaseException, UserNotFoundException, OrganizationNotFoundException,
    PatientNotFoundException, VisitNotFoundException, RoleNotFoundException,
    AddressNotFoundException, UserAlreadyExistsException, OrganizationAlreadyExistsException,
    PatientAlreadyExistsException
)
from core.utils.response import error_response


def handle_object_not_found(model_name, object_id=None, message=None):
    """
    Handle object not found scenarios with appropriate exceptions.
    """
    if model_name.lower() == 'user':
        raise UserNotFoundException(object_id, message)
    elif model_name.lower() == 'organization':
        raise OrganizationNotFoundException(object_id, message)
    elif model_name.lower() == 'patient':
        raise PatientNotFoundException(object_id, message)
    elif model_name.lower() == 'visit':
        raise VisitNotFoundException(object_id, message)
    elif model_name.lower() == 'role':
        raise RoleNotFoundException(object_id, message)
    elif model_name.lower() == 'address':
        raise AddressNotFoundException(object_id, message)
    else:
        raise ResourceNotFoundException(model_name, object_id, message)


def handle_validation_error(field_errors=None, message=None):
    """
    Handle validation errors with detailed field information.
    """
    raise ValidationException(message, field_errors)


def handle_business_logic_error(message=None, business_rule=None):
    """
    Handle business logic violations.
    """
    raise BusinessLogicException(message, business_rule)


def handle_database_error(operation=None, message=None):
    """
    Handle database operation errors.
    """
    raise DatabaseException(message, operation)


def handle_duplicate_error(model_name, identifier=None, message=None):
    """
    Handle duplicate entry errors.
    """
    if model_name.lower() == 'user':
        raise UserAlreadyExistsException(identifier, message)
    elif model_name.lower() == 'organization':
        raise OrganizationAlreadyExistsException(identifier, message)
    elif model_name.lower() == 'patient':
        raise PatientAlreadyExistsException(identifier, message)
    else:
        raise BusinessLogicException(message or f"{model_name} already exists")


def safe_get_object_or_404(model, **kwargs):
    """
    Safely get an object or raise appropriate 404 exception.
    """
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        model_name = model.__name__
        object_id = kwargs.get('id') or kwargs.get('pk')
        handle_object_not_found(model_name, object_id)


def handle_integrity_error(exception, model_name=None):
    """
    Handle database integrity errors with meaningful messages.
    """
    error_message = str(exception)
    
    if 'UNIQUE constraint failed' in error_message:
        if 'email' in error_message.lower():
            raise UserAlreadyExistsException(message="User with this email already exists")
        elif 'name' in error_message.lower():
            raise OrganizationAlreadyExistsException(message="Organization with this name already exists")
        else:
            raise BusinessLogicException("Duplicate entry found")
    elif 'FOREIGN KEY constraint failed' in error_message:
        raise BusinessLogicException("Referenced object does not exist")
    else:
        raise DatabaseException("Database constraint violation")


def create_error_response(error_code, message, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response.
    """
    return error_response(
        error_code=error_code,
        message=message,
        details=details,
        status_code=status_code
    )


def log_and_raise_exception(logger, exception, context=None):
    """
    Log an exception and re-raise it with context.
    """
    if context:
        logger.error(f"{exception}: {context}")
    else:
        logger.error(str(exception))
    raise exception


def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present in the data.
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing_fields.append(field)
    
    if missing_fields:
        raise ValidationException(
            message="Required fields are missing",
            field_errors={field: "This field is required" for field in missing_fields}
        )


def validate_email_format(email):
    """
    Validate email format.
    """
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationException(
            message="Invalid email format",
            field_errors={'email': "Please enter a valid email address"}
        )


def validate_phone_format(phone):
    """
    Validate phone number format.
    """
    import re
    phone_pattern = r'^\+?1?\d{9,15}$'
    if phone and not re.match(phone_pattern, phone):
        raise ValidationException(
            message="Invalid phone number format",
            field_errors={'phone': "Please enter a valid phone number"}
        )


def validate_password_strength(password):
    """
    Validate password strength.
    """
    if len(password) < 8:
        raise ValidationException(
            message="Password is too short",
            field_errors={'password': "Password must be at least 8 characters long"}
        )
    
    if not any(c.isupper() for c in password):
        raise ValidationException(
            message="Password must contain at least one uppercase letter",
            field_errors={'password': "Password must contain at least one uppercase letter"}
        )
    
    if not any(c.islower() for c in password):
        raise ValidationException(
            message="Password must contain at least one lowercase letter",
            field_errors={'password': "Password must contain at least one lowercase letter"}
        )
    
    if not any(c.isdigit() for c in password):
        raise ValidationException(
            message="Password must contain at least one digit",
            field_errors={'password': "Password must contain at least one digit"}
        )
