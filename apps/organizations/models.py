from django.db import models


class Organization(models.Model):
    """
    Organization model for hospitals and clinics.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    TYPE_CHOICES = [
        ('Hospital', 'Hospital'),
        ('Clinic', 'Clinic'),
        ('Laboratory', 'Laboratory'),
        ('Pharmacy', 'Pharmacy'),
        ('Other', 'Other'),
    ]
    
    # Use regular auto-increment ID instead of UUID
    # id = models.AutoField(primary_key=True)  # Django creates this automatically
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Hospital')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    address = models.ForeignKey(
        'addresses.Address',
        on_delete=models.CASCADE,
        related_name='organizations'
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        """Check if the organization is active."""
        return self.status == 'active'
    
    def soft_delete(self):
        """Soft delete the organization."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restore the organization."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()
