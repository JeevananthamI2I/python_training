from rest_framework import serializers
from .models import Visit
from django.utils import timezone


class VisitSerializer(serializers.ModelSerializer):
    """Serializer for Visit model."""
    
    class Meta:
        model = Visit
        fields = [
            'id', 'patient', 'doctor', 'technician', 'organization',
            'scheduled_date', 'actual_date', 'status', 'priority',
            'symptoms', 'diagnosis', 'prescription', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_scheduled_date(self, value):
        """Validate scheduled date."""
        if value and value < timezone.now():
            raise serializers.ValidationError("Scheduled date cannot be in the past.")
        return value
    
    def validate(self, data):
        """Validate visit data."""
        if not data.get('patient'):
            raise serializers.ValidationError("Patient is required.")
        if not data.get('doctor'):
            raise serializers.ValidationError("Doctor is required.")
        if not data.get('organization'):
            raise serializers.ValidationError("Organization is required.")
        return data 