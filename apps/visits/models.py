from django.db import models


class Visit(models.Model):
    """
    Visit model for patient visits and appointments.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='visits'
    )
    doctor = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='doctor_visits'
    )
    technician = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='technician_visits',
        null=True,
        blank=True
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='visits'
    )
    scheduled_date = models.DateTimeField()
    actual_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'visits'
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"Visit {self.id} - {self.patient.name} ({self.get_status_display()})"
    
    @property
    def is_completed(self):
        """Check if the visit is completed."""
        return self.status == 'completed'
    
    @property
    def is_cancelled(self):
        """Check if the visit is cancelled."""
        return self.status == 'cancelled'
    
    @property
    def patient_name(self):
        """Return the patient name."""
        return self.patient.name if self.patient else None
    
    @property
    def doctor_name(self):
        """Return the doctor name."""
        return self.doctor.full_name if self.doctor else None
    
    @property
    def technician_name(self):
        """Return the technician name."""
        return self.technician.full_name if self.technician else None
    
    @property
    def organization_name(self):
        """Return the organization name."""
        return self.organization.name if self.organization else None
    
    def soft_delete(self):
        """Soft delete the visit."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.status = 'cancelled'
        self.save()
    
    def restore(self):
        """Restore the visit."""
        self.is_deleted = False
        self.deleted_at = None
        self.status = 'scheduled'
        self.save()
