"""
Result models for KIU Result Management System
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from apps.students.models import Student
from apps.academics.models import Course, Semester
from .utils import GPACalculator


class Result(models.Model):
    """Student result for a specific course/module"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='results')
    
    # Scores
    coursework_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text='Coursework score (out of 30)'
    )
    final_exam_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(70)],
        help_text='Final exam score (out of 70)'
    )
    
    # Calculated fields
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=2, null=True, blank=True)
    grade_point = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    remark = models.CharField(max_length=50, null=True, blank=True)
    
    # Metadata
    is_published = models.BooleanField(
        default=True,  # CHANGE: Set default to True so results show immediately
        help_text='Mark to publish result for student viewing.'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='uploaded_results'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
        ordering = ['student', 'semester', 'course']
        unique_together = ['student', 'course', 'semester']
    
    def __str__(self):
        return f"{self.student} - {self.course.code} - {self.grade}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate total score, grade, and grade point"""
        # Calculate total score
        if self.coursework_score is not None and self.final_exam_score is not None:
            self.total_score = self.coursework_score + self.final_exam_score
        elif self.total_score is None:
            self.total_score = 0
        
        # Calculate grade information
        if self.total_score is not None:
            grade_info = GPACalculator.get_grade_info(float(self.total_score))
            self.grade = grade_info['grade']
            self.grade_point = grade_info['grade_point']
            self.remark = grade_info['remark']
        
        super().save(*args, **kwargs)


class GPAReport(models.Model):
    """Stored GPA calculations for students"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='gpa_reports')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='gpa_reports')
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    total_credit_units = models.IntegerField(default=0)
    total_grade_points = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'GPA Report'
        verbose_name_plural = 'GPA Reports'
        ordering = ['student', 'semester']
        unique_together = ['student', 'semester']
    
    def __str__(self):
        return f"{self.student} - {self.semester} - GPA: {self.gpa}"