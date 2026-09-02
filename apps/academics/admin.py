"""
Admin configuration for academics app
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Department, Semester, Course


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for Department model."""
    
    list_display = ['name', 'code', 'get_student_count', 'get_course_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code']
    ordering = ['name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'code')
        }),
        (_('Additional Information'), {
            'fields': ('description',)
        }),
    )
    
    def get_student_count(self, obj):
        """Display student count in list."""
        return obj.get_student_count()
    get_student_count.short_description = 'Students'
    
    def get_course_count(self, obj):
        """Display course count in list."""
        return obj.get_course_count()
    get_course_count.short_description = 'Courses'


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    """Admin interface for Semester model."""
    
    list_display = [
        'name', 
        'academic_year', 
        'semester_number',
        'is_active',
        'is_result_published',
        'get_result_count'
    ]
    list_filter = ['academic_year', 'semester_number', 'is_active', 'is_result_published']
    search_fields = ['name', 'academic_year']
    ordering = ['-academic_year', 'semester_number']
    
    fieldsets = (
        (None, {
            'fields': ('academic_year', 'semester_number', 'name')
        }),
        (_('Dates'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_result_published')
        }),
    )
    
    actions = ['publish_results', 'unpublish_results']
    
    def get_result_count(self, obj):
        """Display result count in list."""
        return obj.get_result_count()
    get_result_count.short_description = 'Results'
    
    def publish_results(self, request, queryset):
        """Publish results for selected semesters."""
        updated = queryset.update(is_result_published=True)
        self.message_user(request, f'{updated} semester(s) results published.')
    publish_results.short_description = "Publish results for selected semesters"
    
    def unpublish_results(self, request, queryset):
        """Unpublish results for selected semesters."""
        updated = queryset.update(is_result_published=False)
        self.message_user(request, f'{updated} semester(s) results unpublished.')
    unpublish_results.short_description = "Unpublish results for selected semesters"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""
    
    list_display = [
        'code',
        'title',
        'department',
        'semester',
        'year_of_study',
        'credit_units',
        'is_elective'
    ]
    list_filter = ['department', 'semester', 'year_of_study', 'is_elective']
    search_fields = ['code', 'title']
    ordering = ['code']
    
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'credit_units')
        }),
        (_('Classification'), {
            'fields': ('department', 'semester', 'year_of_study', 'is_elective')
        }),
        (_('Additional Information'), {
            'fields': ('description',)
        }),
    )