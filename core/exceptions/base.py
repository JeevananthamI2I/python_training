from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    """
    Base custom exception class for the Hospital Management System.
    """
    def __init__(self, message=None, code=None, details=None, status_code=None):
        self.message = message or "An error occurred"
        self.code = code or "unknown_error"
        self.details = details
        self.status_code = status_code or status.HTTP_400_BAD_REQUEST
        super().__init__(self.message)


class ResourceNotFoundException(CustomAPIException):
    """
    Exception raised when a requested resource is not found.
    """
    def __init__(self, resource_type="Resource", resource_id=None, message=None):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.message = message or f"{resource_type} not found"
        if resource_id:
            self.message += f" with ID: {resource_id}"
        super().__init__(
            message=self.message,
            code="resource_not_found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationException(CustomAPIException):
    """
    Exception raised when data validation fails.
    """
    def __init__(self, message=None, field_errors=None):
        self.field_errors = field_errors or {}
        super().__init__(
            message=message or "Validation failed",
            code="validation_error",
            details=self.field_errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class AuthenticationException(CustomAPIException):
    """
    Exception raised when authentication fails.
    """
    def __init__(self, message=None):
        super().__init__(
            message=message or "Authentication failed",
            code="authentication_error",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class PermissionException(CustomAPIException):
    """
    Exception raised when user doesn't have required permissions.
    """
    def __init__(self, message=None, required_permission=None):
        self.required_permission = required_permission
        super().__init__(
            message=message or "Permission denied",
            code="permission_denied",
            status_code=status.HTTP_403_FORBIDDEN
        )


class BusinessLogicException(CustomAPIException):
    """
    Exception raised when business logic rules are violated.
    """
    def __init__(self, message=None, business_rule=None):
        self.business_rule = business_rule
        super().__init__(
            message=message or "Business rule violation",
            code="business_logic_error",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class DatabaseException(CustomAPIException):
    """
    Exception raised when database operations fail.
    """
    def __init__(self, message=None, operation=None):
        self.operation = operation
        super().__init__(
            message=message or "Database operation failed",
            code="database_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ExternalServiceException(CustomAPIException):
    """
    Exception raised when external service calls fail.
    """
    def __init__(self, message=None, service_name=None):
        self.service_name = service_name
        super().__init__(
            message=message or "External service error",
            code="external_service_error",
            status_code=status.HTTP_502_BAD_GATEWAY
        )


class RateLimitException(CustomAPIException):
    """
    Exception raised when rate limits are exceeded.
    """
    def __init__(self, message=None, retry_after=None):
        self.retry_after = retry_after
        super().__init__(
            message=message or "Rate limit exceeded",
            code="rate_limit_exceeded",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )


class ConfigurationException(CustomAPIException):
    """
    Exception raised when there are configuration issues.
    """
    def __init__(self, message=None, config_key=None):
        self.config_key = config_key
        super().__init__(
            message=message or "Configuration error",
            code="configuration_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Specific domain exceptions
class UserNotFoundException(ResourceNotFoundException):
    def __init__(self, user_id=None, message=None):
        super().__init__("User", user_id, message)


class OrganizationNotFoundException(ResourceNotFoundException):
    def __init__(self, org_id=None, message=None):
        super().__init__("Organization", org_id, message)


class PatientNotFoundException(ResourceNotFoundException):
    def __init__(self, patient_id=None, message=None):
        super().__init__("Patient", patient_id, message)


class VisitNotFoundException(ResourceNotFoundException):
    def __init__(self, visit_id=None, message=None):
        super().__init__("Visit", visit_id, message)


class RoleNotFoundException(ResourceNotFoundException):
    def __init__(self, role_id=None, message=None):
        super().__init__("Role", role_id, message)


class AddressNotFoundException(ResourceNotFoundException):
    def __init__(self, address_id=None, message=None):
        super().__init__("Address", address_id, message)


class InvalidCredentialsException(AuthenticationException):
    def __init__(self, message="Invalid email or password"):
        super().__init__(message)


class TokenExpiredException(AuthenticationException):
    def __init__(self, message="Token has expired"):
        super().__init__(message)


class InvalidTokenException(AuthenticationException):
    def __init__(self, message="Invalid token"):
        super().__init__(message)


class UserAlreadyExistsException(BusinessLogicException):
    def __init__(self, email=None, message=None):
        self.email = email
        msg = message or f"User with email {email} already exists" if email else "User already exists"
        super().__init__(msg)


class OrganizationAlreadyExistsException(BusinessLogicException):
    def __init__(self, name=None, message=None):
        self.name = name
        msg = message or f"Organization with name {name} already exists" if name else "Organization already exists"
        super().__init__(msg)


class PatientAlreadyExistsException(BusinessLogicException):
    def __init__(self, identifier=None, message=None):
        self.identifier = identifier
        msg = message or f"Patient with identifier {identifier} already exists" if identifier else "Patient already exists"
        super().__init__(msg) 