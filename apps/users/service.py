from .models import User
from .serializers import UserSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserService:
    """
    Service layer to handle User-related business logic.
    
    This class acts as the gatekeeper between your views/controllers
    and your database models. It validates, creates, updates, and manages
    users in a clean, maintainable way.
    """

    @staticmethod
    def create_user(data):
        """
        Create a new user with the provided data.

        Uses UserSerializer to validate input and save the user.
        Returns a tuple of (User instance or None, validation errors or None).

        Args:
            data (dict): User data payload.

        Returns:
            tuple: (User object or None, errors dict or None)
        """
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return user, None
        return None, serializer.errors

    @staticmethod
    def get_user(user_id):
        """
        Retrieve a user by ID.

        Returns None if no user exists with the given ID.

        Args:
            user_id (int): The primary key of the user.

        Returns:
            User or None
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def list_users():
        """
        Fetch all users.

        Returns:
            QuerySet: All User objects.
        """
        return User.objects.all()

    @staticmethod
    def update_user(user, data):
        """
        Update an existing user with partial or full data.

        Uses UserSerializer for validation and update.
        Returns a tuple of (User instance or None, validation errors or None).

        Args:
            user (User): The User instance to update.
            data (dict): Partial or full user data to update.

        Returns:
            tuple: (User object or None, errors dict or None)
        """
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return user, None
        return None, serializer.errors

    @staticmethod
    def delete_user(user, soft_delete=True):
        """
        Delete a user.

        Performs a soft delete if the User model supports it and soft_delete is True,
        otherwise hard deletes the user record.

        Args:
            user (User): The User instance to delete.
            soft_delete (bool): Flag to soft delete instead of hard delete.

        Returns:
            bool: True if deletion was successful.
        """
        if soft_delete and hasattr(user, 'soft_delete'):
            user.soft_delete()
        else:
            user.delete()
        return True

    @staticmethod
    def change_password(user, new_password):
        """
        Change the user's password after validating it.

        Args:
            user (User): The User instance whose password is to be changed.
            new_password (str): The new password string.

        Returns:
            tuple: (bool indicating success, None or list of validation errors)
        """
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return False, e.messages
        user.set_password(new_password)
        user.save()
        return True, None
