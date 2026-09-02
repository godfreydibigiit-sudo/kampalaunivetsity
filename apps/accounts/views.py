"""
Authentication views for KIU Result Management System
"""
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import UserLoginForm


class UserLoginView(LoginView):
    """
    Custom login view for students.
    """
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = False
    
    def get_success_url(self):
        """Redirect based on user type after login."""
        user = self.request.user
        
        # If admin user logs in from student login page, go to admin
        if user.is_superuser or user.is_staff:
            return reverse_lazy('admin:index')
        # If student, go to dashboard
        else:
            return reverse_lazy('students:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        """Handle already authenticated users."""
        if request.user.is_authenticated:
            # If already logged in, go to appropriate page
            if request.user.is_superuser or request.user.is_staff:
                return redirect('admin:index')
            else:
                return redirect('students:dashboard')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Handle successful login."""
        user = form.get_user()
        messages.success(self.request, f'Welcome back, {user.get_full_name()}!')
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """
    Custom logout view.
    """
    next_page = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)