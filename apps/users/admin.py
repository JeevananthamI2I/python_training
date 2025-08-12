from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin interface for User model."""
    
    list_display = [
        'email', 'full_name', 'organization_name', 'role_name', 
        'status', 'is_active', 'created_at', 'last_login'
    ]
    list_filter = [
        'status', 'is_active', 'is_staff', 'is_superuser', 
        'organization', 'role', 'gender', 'created_at'
    ]
    search_fields = ['email', 'username', 'phone']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
    
    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Info', {
            'fields': ('phone', 'gender', 'date_of_birth')
        }),
        ('Organization & Role', {
            'fields': ('organization', 'role')
        }),
        ('Status & Permissions', {
            'fields': ('status', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    def full_name(self, obj):
        """Display full name with styling."""
        return format_html(
            '<strong>{}</strong>',
            obj.full_name
        )
    full_name.short_description = 'Full Name'
    
    def organization_name(self, obj):
        """Display organization name."""
        return obj.organization_name or '-'
    organization_name.short_description = 'Organization'
    
    def role_name(self, obj):
        """Display role name."""
        return obj.role_name or '-'
    role_name.short_description = 'Role'
    
    def get_queryset(self, request):
        """Filter out soft-deleted users by default."""
        return super().get_queryset(request).filter(is_deleted=False)
    
    actions = ['activate_users', 'deactivate_users', 'soft_delete_users', 'restore_users']
    
    def activate_users(self, request, queryset):
        """Activate selected users."""
        updated = queryset.update(status='active', is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users."""
        updated = queryset.update(status='inactive', is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def soft_delete_users(self, request, queryset):
        """Soft delete selected users."""
        for user in queryset:
            user.soft_delete()
        self.message_user(request, f'{queryset.count()} users were successfully soft deleted.')
    soft_delete_users.short_description = "Soft delete selected users"
    
    def restore_users(self, request, queryset):
        """Restore soft-deleted users."""
        for user in queryset:
            user.restore()
        self.message_user(request, f'{queryset.count()} users were successfully restored.')
    restore_users.short_description = "Restore selected users"
