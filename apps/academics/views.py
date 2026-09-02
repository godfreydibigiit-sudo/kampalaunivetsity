"""
Views for academics app
Mostly handled by Django Admin, but included for future expansion.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Department, Semester, Course


@login_required
def course_list(request):
    """View to list all courses (for future expansion)."""
    courses = Course.objects.all().select_related('department', 'semester')
    context = {'courses': courses}
    return render(request, 'academics/course_list.html', context)