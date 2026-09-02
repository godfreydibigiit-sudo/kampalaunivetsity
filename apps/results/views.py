"""
Result views for KIU Result Management System
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView
from apps.students.models import Student
from apps.academics.models import Semester
from .models import Result, GPAReport
from .utils import GPACalculator
from .pdf_generator import ResultPDFGenerator


@method_decorator(login_required, name='dispatch')
class StudentResultsView(ListView):
    """
    Display all results for the logged-in student.
    """
    template_name = 'results/student_results.html'
    context_object_name = 'semester_results'
    
    def get_queryset(self):
        """Get student and their results grouped by semester."""
        student = get_object_or_404(Student, user=self.request.user)
        
        # Get all published semesters
        semesters = Semester.objects.filter(
            is_result_published=True
        ).order_by('academic_year', 'semester_number')
        
        semester_data = []
        cumulative_points = 0
        cumulative_credits = 0
        
        for semester in semesters:
            results = Result.objects.filter(
                student=student,
                semester=semester,
                is_published=True
            ).select_related('course')
            
            if results.exists():
                gpa = GPACalculator.calculate_semester_gpa(results)
                total_credits = sum(r.course.credit_units for r in results)
                
                semester_data.append({
                    'semester': semester,
                    'results': results,
                    'gpa': gpa,
                    'total_credits': total_credits,
                })
                
                # Cumulative calculation
                cumulative_points += gpa * total_credits
                cumulative_credits += total_credits
        
        # Calculate CGPA
        cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0
        
        return {
            'semesters': semester_data,
            'cgpa': round(cgpa, 2),
            'student': student,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_data = self.get_queryset()
        context.update(queryset_data)
        return context


@method_decorator(login_required, name='dispatch')
class ResultDetailView(DetailView):
    """
    Display detailed results for a specific semester.
    """
    template_name = 'results/result_detail.html'
    context_object_name = 'semester_data'
    
    def get_object(self):
        """Get semester results for current student."""
        student = get_object_or_404(Student, user=self.request.user)
        semester_id = self.kwargs.get('semester_id')
        semester = get_object_or_404(
            Semester,
            id=semester_id,
            is_result_published=True
        )
        
        results = Result.objects.filter(
            student=student,
            semester=semester,
            is_published=True
        ).select_related('course')
        
        gpa = GPACalculator.calculate_semester_gpa(results)
        
        return {
            'semester': semester,
            'results': results,
            'gpa': gpa,
            'student': student,
            'total_credits': sum(r.course.credit_units for r in results),
        }


@login_required
def download_result_pdf(request, semester_id):
    """
    Download results for a specific semester as PDF.
    """
    student = get_object_or_404(Student, user=request.user)
    semester = get_object_or_404(
        Semester,
        id=semester_id,
        is_result_published=True
    )
    
    results = Result.objects.filter(
        student=student,
        semester=semester,
        is_published=True
    ).select_related('course')
    
    gpa = GPACalculator.calculate_semester_gpa(results)
    
    results_data = {
        'semester': semester,
        'results': results,
        'gpa': gpa,
        'total_credits': sum(r.course.credit_units for r in results),
    }
    
    pdf_content = ResultPDFGenerator.generate_result_pdf(student, results_data)
    
    if pdf_content:
        filename = f"results_{student.user.registration_number}_{semester.academic_year}_{semester.semester_number}.pdf"
        return ResultPDFGenerator.download_pdf_response(pdf_content, filename)
    else:
        messages.error(request, 'Error generating PDF. Please try again.')
        return redirect('results:view_results')


@login_required
def download_transcript_pdf(request):
    """
    Download complete academic transcript as PDF.
    """
    student = get_object_or_404(Student, user=request.user)
    
    semesters = Semester.objects.filter(
        is_result_published=True
    ).order_by('academic_year', 'semester_number')
    
    all_semesters_data = []
    
    for semester in semesters:
        results = Result.objects.filter(
            student=student,
            semester=semester,
            is_published=True
        ).select_related('course')
        
        if results.exists():
            gpa = GPACalculator.calculate_semester_gpa(results)
            all_semesters_data.append({
                'semester': semester,
                'results': results,
                'gpa': gpa,
            })
    
    pdf_content = ResultPDFGenerator.generate_transcript(all_semesters_data, student)
    
    if pdf_content:
        filename = f"transcript_{student.user.registration_number}.pdf"
        return ResultPDFGenerator.download_pdf_response(pdf_content, filename)
    else:
        messages.error(request, 'Error generating transcript. Please try again.')
        return redirect('results:view_results')