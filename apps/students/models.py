"""
Student models for KIU Result Management System
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.academics.models import Department


class Student(models.Model):
    """
    Student profile model extending the User model.
    """
    
    class YearOfStudy(models.IntegerChoices):
        YEAR_1 = 1, 'Year 1'
        YEAR_2 = 2, 'Year 2'
        YEAR_3 = 3, 'Year 3'
        YEAR_4 = 4, 'Year 4'
        YEAR_5 = 5, 'Year 5'
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name=_('User'),
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name=_('Department'),
    )
    year_of_study = models.IntegerField(
        _('Year of Study'),
        choices=YearOfStudy.choices,
        default=YearOfStudy.YEAR_1,
    )
    enrollment_year = models.IntegerField(
        _('Enrollment Year'),
        default=2024,
        help_text='Year when student enrolled (e.g., 2024)',
    )
    guardian_name = models.CharField(
        _('Guardian Name'),
        max_length=255,
        blank=True,
        null=True,
    )
    guardian_phone = models.CharField(
        _('Guardian Phone'),
        max_length=20,
        blank=True,
        null=True,
    )
    address = models.TextField(
        _('Address'),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True,
    )
    
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['user__registration_number']
    
    def __str__(self):
        """FIXED: Simple string representation"""
        if self.user and self.user.full_name:
            return f"{self.user.registration_number} - {self.user.full_name}"
        elif self.user:
            return self.user.registration_number
        return f"Student {self.id}"
    
    def get_full_name(self):
        """Return student's full name."""
        return self.user.get_full_name() if self.user else ""
    
    def get_registration_number(self):
        """Return student's registration number."""
        return self.user.registration_number if self.user else ""
    
    def get_department_name(self):
        """Return department name or 'Not Assigned'."""
        return self.department.name if self.department else 'Not Assigned'
    
    def get_year_of_study_display(self):
        """Return year of study as string."""
        return f'Year {self.year_of_study}'
    
    @property
    def email(self):
        """Get student's email."""
        return self.user.email if self.user else ""
    
    @property
    def phone_number(self):
        """Get student's phone number."""
        return self.user.phone_number if self.user else ""