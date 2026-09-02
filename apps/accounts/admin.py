"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for User model.
    """
    
    # Fields to display in list
    list_display = [
        'registration_number', 
        'full_name', 
        'email', 
        'user_type',
        'is_active', 
        'is_verified',
        'date_joined'
    ]
    
    # Filters
    list_filter = [
        'user_type', 
        'is_active', 
        'is_staff', 
        'is_verified',
        'date_joined'
    ]
    
    # Search fields
    search_fields = [
        'registration_number', 
        'full_name', 
        'email'
    ]
    
    # Ordering
    ordering = ['registration_number']
    
    # Fieldsets for viewing/editing users
    fieldsets = (
        (None, {
            'fields': ('registration_number', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        (_('User Type'), {
            'fields': ('user_type',)
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'is_verified',
                'groups', 
                'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fieldsets for adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'registration_number', 
                'email', 
                'full_name',
                'user_type',
                'password1', 
                'password2'
            ),
        }),
    )
    
    # Make fields read-only after creation
    readonly_fields = ['date_joined', 'last_login']
    
    # Actions
    actions = ['verify_users', 'unverify_users', 'activate_users', 'deactivate_users']
    
    def verify_users(self, request, queryset):
        """Mark selected users as verified."""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} user(s) marked as verified.')
    verify_users.short_description = "Mark selected users as verified"
    
    def unverify_users(self, request, queryset):
        """Mark selected users as unverified."""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} user(s) marked as unverified.')
    unverify_users.short_description = "Mark selected users as unverified"
    
    def activate_users(self, request, queryset):
        """Activate selected users."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated.')
    deactivate_users.short_description = "Deactivate selected users"