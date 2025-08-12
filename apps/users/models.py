from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    # username: optional, unique, max_length like default Django (150)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    # email unique for login
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )

    role = models.ForeignKey(
        'roles.Role',
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )

    address = models.ForeignKey(
        'addresses.Address',
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email to login
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return the user's username or email as fallback."""
        return self.username if self.username else self.email

    @property
    def is_active_user(self):
        return self.status == 'active' and self.is_active

    @property
    def organization_name(self):
        return self.organization.name if self.organization else None

    @property
    def role_name(self):
        return self.role.name if self.role else None

    @property
    def is_admin(self):
        return self.role and self.role.name.lower() in ['admin', 'super_admin', 'hospital_admin']

    def can_bypass_organization_validation(self):
        return self.is_admin and not self.organization

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.is_active = True
        self.save()
