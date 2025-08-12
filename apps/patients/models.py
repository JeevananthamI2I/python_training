from django.db import models


class Patient(models.Model):
    """
    Patient model for patient records.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deceased', 'Deceased'),
    ]
    
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='patients'
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='created_patients',
        null=True,
        blank=True
    )
    address = models.ForeignKey(
        'addresses.Address',
        on_delete=models.SET_NULL,
        related_name='patients',
        null=True,
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.age} years, {self.get_gender_display()})"
    
    @property
    def is_active_patient(self):
        """Check if the patient is active."""
        return self.status == 'active'
    
    @property
    def organization_name(self):
        """Return the organization name."""
        return self.organization.name if self.organization else None
    
    @property
    def created_by_name(self):
        """Return the name of the user who created this patient."""
        return self.created_by.full_name if self.created_by else None
    
    def soft_delete(self):
        """Soft delete the patient."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.status = 'inactive'
        self.save()
    
    def restore(self):
        """Restore the patient."""
        self.is_deleted = False
        self.deleted_at = None
        self.status = 'active'
        self.save()
