from django.contrib import admin
from .models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role model."""
    list_display = ['name', 'description', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'permissions')
        }),
        ('Status', {
            'fields': ('is_active', 'is_deleted', 'deleted_at')
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_roles', 'deactivate_roles', 'soft_delete_roles', 'restore_roles']
    
    def activate_roles(self, request, queryset):
        """Activate selected roles."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} roles were successfully activated.')
    activate_roles.short_description = "Activate selected roles"
    
    def deactivate_roles(self, request, queryset):
        """Deactivate selected roles."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} roles were successfully deactivated.')
    deactivate_roles.short_description = "Deactivate selected roles"
    
    def soft_delete_roles(self, request, queryset):
        """Soft delete selected roles."""
        from django.utils import timezone
        updated = queryset.update(is_deleted=True, deleted_at=timezone.now())
        self.message_user(request, f'{updated} roles were successfully deleted.')
    soft_delete_roles.short_description = "Soft delete selected roles"
    
    def restore_roles(self, request, queryset):
        """Restore selected roles."""
        updated = queryset.update(is_deleted=False, deleted_at=None)
        self.message_user(request, f'{updated} roles were successfully restored.')
    restore_roles.short_description = "Restore selected roles"
    
    def get_queryset(self, request):
        """Filter out soft deleted roles by default."""
        return super().get_queryset(request).filter(is_deleted=False)
