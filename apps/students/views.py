"""
Student views for KIU Result Management System
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.results.models import Result
from apps.academics.models import Semester
from apps.results.utils import GPACalculator
from .models import Student
from .forms import StudentProfileForm


@method_decorator(login_required, name='dispatch')
class StudentDashboardView(TemplateView):
    """Student dashboard showing module results and GPA"""
    template_name = 'students/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get or create student profile
        student, created = Student.objects.get_or_create(user=user)
        
        # Get ALL semesters (not just published ones)
        semesters = Semester.objects.all().order_by('academic_year', 'semester_number')
        
        semester_data = []
        all_results = []
        
        for semester in semesters:
            # Get ALL results (removed is_published filter)
            results = Result.objects.filter(
                student=student,
                semester=semester
            ).select_related('course')
            
            if results.exists():
                # Calculate semester GPA
                gpa = GPACalculator.calculate_semester_gpa(results)
                total_credits = sum(r.course.credit_units for r in results)
                
                # Prepare module results
                module_results = []
                for result in results:
                    module_results.append({
                        'course_code': result.course.code,
                        'course_title': result.course.title,
                        'credit_units': result.course.credit_units,
                        'coursework_score': result.coursework_score,
                        'final_exam_score': result.final_exam_score,
                        'total_score': result.total_score,
                        'grade': result.grade,
                        'grade_point': result.grade_point,
                        'remark': result.remark,
                    })
                
                semester_data.append({
                    'semester': semester,
                    'module_results': module_results,
                    'gpa': gpa,
                    'total_credits': total_credits,
                })
                
                all_results.extend(results)
        
        # Calculate CGPA
        cgpa = GPACalculator.calculate_cgpa(all_results)
        classification = GPACalculator.get_gpa_classification(cgpa)
        
        context.update({
            'student': student,
            'semester_data': semester_data,
            'cgpa': cgpa,
            'classification': classification,
            'total_semesters': len(semester_data),
            'total_modules': len(all_results),
        })
        
        return context


@method_decorator(login_required, name='dispatch')
class StudentProfileView(UpdateView):
    """View for editing student profile"""
    model = Student
    form_class = StudentProfileForm
    template_name = 'students/profile.html'
    success_url = reverse_lazy('students:profile')
    
    def get_object(self, queryset=None):
        student, created = Student.objects.get_or_create(user=self.request.user)
        return student
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)