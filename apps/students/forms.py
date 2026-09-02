"""
Student forms for KIU Result Management System
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Student
from apps.accounts.models import User


class StudentProfileForm(forms.ModelForm):
    """
    Form for updating student profile information.
    """
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name',
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
        }),
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number',
        }),
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        }),
    )
    
    class Meta:
        model = Student
        fields = [
            'department',
            'year_of_study',
            'guardian_name',
            'guardian_phone',
            'address',
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter guardian name',
            }),
            'guardian_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter guardian phone',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter address',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize form with current user data."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Set initial values for user fields
            self.fields['full_name'].initial = self.user.full_name
            self.fields['email'].initial = self.user.email
            self.fields['phone_number'].initial = self.user.phone_number
    
    def save(self, commit=True):
        """Save both User and Student models."""
        student = super().save(commit=False)
        
        # Update User model fields
        if self.user:
            self.user.full_name = self.cleaned_data['full_name']
            self.user.email = self.cleaned_data['email']
            self.user.phone_number = self.cleaned_data['phone_number']
            if self.cleaned_data.get('profile_picture'):
                self.user.profile_picture = self.cleaned_data['profile_picture']
            if commit:
                self.user.save()
        
        if commit:
            student.save()
        
        return student