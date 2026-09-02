"""
PDF generation utilities for KIU Result Management System
"""
import os
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse


class ResultPDFGenerator:
    """
    Generate PDF result reports for students.
    """
    
    @staticmethod
    def generate_result_pdf(student, results_data):
        """
        Generate PDF for student results.
        
        Args:
            student: Student object
            results_data: Dictionary containing results info
        
        Returns:
            PDF file content
        """
        template_path = 'results/result_pdf.html'
        context = {
            'student': student,
            'results_data': results_data,
            'university_name': 'Kampala International University',
            'university_address': 'Kampala, Uganda',
        }
        
        # Render HTML template
        html = render_to_string(template_path, context)
        
        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(
            BytesIO(html.encode("UTF-8")),
            result,
            encoding='UTF-8'
        )
        
        if not pdf.err:
            return result.getvalue()
        return None
    
    @staticmethod
    def download_pdf_response(pdf_content, filename):
        """
        Create HTTP response with PDF download.
        """
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    @staticmethod
    def generate_transcript(all_semesters_data, student):
        """
        Generate complete academic transcript.
        
        Args:
            all_semesters_data: List of semester data dictionaries
            student: Student object
        
        Returns:
            PDF file content
        """
        template_path = 'results/transcript_pdf.html'
        context = {
            'student': student,
            'semesters': all_semesters_data,
            'university_name': 'Kampala International University',
        }
        
        html = render_to_string(template_path, context)
        
        result = BytesIO()
        pdf = pisa.pisaDocument(
            BytesIO(html.encode("UTF-8")),
            result,
            encoding='UTF-8'
        )
        
        if not pdf.err:
            return result.getvalue()
        return None