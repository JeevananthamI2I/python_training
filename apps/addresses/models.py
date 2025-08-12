from django.db import models


class Address(models.Model):
    """
    Address model for organizations, users, and patients.
    """
    # Use regular auto-increment ID instead of UUID
    # id = models.AutoField(primary_key=True)  # Django creates this automatically
    
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"
    
    @property
    def full_address(self):
        """Return the complete address as a string."""
        parts = []
        if self.street_address:
            parts.append(self.street_address)
        parts.extend([self.city, self.state, self.pincode, self.country])
        return ', '.join(filter(None, parts))
    
    def soft_delete(self):
        """Soft delete the address."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restore the address."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()
