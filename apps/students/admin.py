"""
Admin configuration for students app
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin interface for Student model.
    """
    
    list_display = [
        'user',
        'department',
        'year_of_study',
        'enrollment_year',
        'created_at',
    ]
    
    list_filter = [
        'department',
        'year_of_study',
        'enrollment_year',
    ]
    
    search_fields = [
        'user__registration_number',
        'user__full_name',
        'user__email',
    ]
    
    raw_id_fields = ['user']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'department', 'year_of_study')
        }),
        (_('Additional Information'), {
            'fields': ('guardian_name', 'guardian_phone', 'address')
        }),
        (_('Important Dates'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        """Make user field readonly after creation."""
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:  # If editing existing object
            readonly.append('user')
        return readonly