"""
Authentication forms for KIU Result Management System
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class UserLoginForm(AuthenticationForm):
    """
    Custom login form for user authentication.
    """
    username = forms.CharField(
        label='Registration Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registration number',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'current-password',
        }),
    )
    
    error_messages = {
        'invalid_login': (
            "Invalid registration number or password. "
            "Please try again or contact the administrator."
        ),
        'inactive': "This account is inactive. Please contact the administrator.",
    }
    
    def clean(self):
        """Custom clean method to handle custom authentication."""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return cleaned_data
    
    def confirm_login_allowed(self, user):
        """Override to add custom user validation."""
        super().confirm_login_allowed(user)
        if not user.is_verified:
            raise forms.ValidationError(
                "Your account is not verified. Please contact the administrator.",
                code='unverified',
            )