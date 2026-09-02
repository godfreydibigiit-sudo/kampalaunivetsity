"""
Custom User model for KIU Result Management System
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model"""
    
    ADMIN = 'ADMIN'
    STUDENT = 'STUDENT'
    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
    ]
    
    registration_number = models.CharField(
        _('Registration Number'),
        max_length=50,
        unique=True,
    )
    email = models.EmailField(
        _('Email Address'),
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(
        _('Full Name'),
        max_length=255,
        blank=True,
        null=True,
    )
    user_type = models.CharField(
        _('User Type'),
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=STUDENT,
    )
    
    # Django required fields
    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
    )
    is_verified = models.BooleanField(
        _('Verified'),
        default=True,
    )
    
    # Timestamps
    date_joined = models.DateTimeField(
        _('Date Joined'),
        default=timezone.now,
    )
    last_login = models.DateTimeField(
        _('Last Login'),
        null=True,
        blank=True,
    )
    
    # Additional fields
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=20,
        blank=True,
        null=True,
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.registration_number}"
    
    def get_full_name(self):
        return self.full_name or self.registration_number
    
    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.registration_number
    
    # Required methods
    def is_admin(self):
        """Check if user is admin"""
        return self.user_type == self.ADMIN or self.is_superuser or self.is_staff
    
    def is_student(self):
        """Check if user is student"""
        return self.user_type == self.STUDENT
    
    # Properties
    @property
    def is_admin_user(self):
        """Property to check if user is admin"""
        return self.is_admin()
    
    @property
    def is_student_user(self):
        """Property to check if user is student"""
        return self.is_student()
    
    # Required for Django admin
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True
    
    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True