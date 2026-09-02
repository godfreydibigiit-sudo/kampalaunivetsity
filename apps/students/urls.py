"""
URL patterns for students app
"""
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.StudentDashboardView.as_view(), name='dashboard'),
    path('profile/', views.StudentProfileView.as_view(), name='profile'),
]