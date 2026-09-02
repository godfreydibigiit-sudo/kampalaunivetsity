"""
Academic models for KIU Result Management System
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Department(models.Model):
    """Academic department model"""
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_student_count(self):
        """Return number of students in this department"""
        return self.students.count()
    
    def get_course_count(self):
        """Return number of courses in this department"""
        return self.courses.count()


class Semester(models.Model):
    """Academic semester model"""
    
    class SemesterNumber(models.IntegerChoices):
        SEMESTER_ONE = 1, 'Semester One'
        SEMESTER_TWO = 2, 'Semester Two'
    
    name = models.CharField(max_length=100, blank=True)
    academic_year = models.CharField(max_length=20)
    semester_number = models.IntegerField(choices=SemesterNumber.choices, default=SemesterNumber.SEMESTER_ONE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_result_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'
        ordering = ['academic_year', 'semester_number']
        unique_together = ['academic_year', 'semester_number']
    
    def __str__(self):
        if self.name:
            return self.name
        return f"{self.get_semester_number_display()} - {self.academic_year}"
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"{self.get_semester_number_display()} {self.academic_year}"
        super().save(*args, **kwargs)
    
    # ADD THIS METHOD
    def get_result_count(self):
        """Return number of results for this semester"""
        return self.results.count()
    
    # ADD THIS METHOD TOO
    def get_course_count(self):
        """Return number of courses in this semester"""
        return self.courses.count()


class Course(models.Model):
    """Course/Module model"""
    
    class YearOfStudy(models.IntegerChoices):
        YEAR_1 = 1, 'Year 1'
        YEAR_2 = 2, 'Year 2'
        YEAR_3 = 3, 'Year 3'
        YEAR_4 = 4, 'Year 4'
        YEAR_5 = 5, 'Year 5'
    
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    credit_units = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    year_of_study = models.IntegerField(choices=YearOfStudy.choices, default=YearOfStudy.YEAR_1)
    is_elective = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Course/Module'
        verbose_name_plural = 'Courses/Modules'
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    # ADD THIS METHOD
    def get_result_count(self):
        """Return number of results for this course"""
        return self.results.count()