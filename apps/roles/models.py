from django.db import models


class Role(models.Model):
    """
    Role model for user roles in the system.
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('hospital_admin', 'Hospital Admin'),
        ('admin', 'Admin'),  # Add admin role
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('technician', 'Technician'),
        ('receptionist', 'Receptionist'),
        ('viewer', 'Viewer'),
    ]
    
    # Use regular auto-increment ID instead of UUID
    # id = models.AutoField(primary_key=True)  # Django creates this automatically
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def soft_delete(self):
        """Soft delete the role."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restore the soft deleted role."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()
