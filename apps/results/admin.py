"""
Admin configuration for results app
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Result, GPAReport
from .utils import GPACalculator


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Admin interface for Result model"""
    
    list_display = [
        'student',
        'course',
        'semester',
        'coursework_score',
        'final_exam_score',
        'total_score',
        'grade',
        'grade_point',
        'is_published',
    ]
    
    list_filter = [
        'semester',
        'grade',
        'is_published',
        'course__department',
    ]
    
    search_fields = [
        'student__user__registration_number',
        'student__user__full_name',
        'course__code',
        'course__title',
    ]
    
    raw_id_fields = ['student']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'course', 'semester')
        }),
        ('Module Scores', {
            'fields': ('coursework_score', 'final_exam_score'),
            'description': 'Enter coursework (out of 30) and final exam (out of 70) scores'
        }),
        ('Calculated Results', {
            'fields': ('total_score', 'grade', 'grade_point', 'remark'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_published', 'uploaded_by')
        }),
    )
    
    readonly_fields = ['total_score', 'grade', 'grade_point', 'remark']
    
    def save_model(self, request, obj, form, change):
        """Set uploaded_by and auto-publish"""
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        # Auto-publish results
        obj.is_published = True
        super().save_model(request, obj, form, change)
    
    actions = ['publish_results', 'unpublish_results']
    
    def publish_results(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} result(s) published for students to view.')
    publish_results.short_description = "Publish selected results for students"
    
    def unpublish_results(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} result(s) unpublished.')
    unpublish_results.short_description = "Unpublish selected results"


@admin.register(GPAReport)
class GPAReportAdmin(admin.ModelAdmin):
    """Admin interface for GPA Report model"""
    
    list_display = ['student', 'semester', 'gpa', 'total_credit_units', 'total_grade_points', 'created_at']
    list_filter = ['semester', 'created_at']
    search_fields = ['student__user__registration_number', 'student__user__full_name']
    readonly_fields = ['gpa', 'total_credit_units', 'total_grade_points']