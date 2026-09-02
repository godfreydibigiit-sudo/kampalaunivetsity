"""
URL patterns for accounts app
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Login URL (also accessible at /accounts/login/)
    path('login/', views.UserLoginView.as_view(), name='login'),
    
    # Logout URL
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]