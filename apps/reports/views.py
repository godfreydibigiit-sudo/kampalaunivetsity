"""
Report views for KIU Result Management System
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.results.models import Result
from apps.students.models import Student


@login_required
def report_dashboard(request):
    """
    Simple report dashboard for students.
    """
    student = Student.objects.get(user=request.user)
    total_results = Result.objects.filter(student=student).count()
    
    context = {
        'student': student,
        'total_results': total_results,
    }
    
    return render(request, 'reports/dashboard.html', context)