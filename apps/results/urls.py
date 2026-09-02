"""
URL patterns for results app
"""
from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('', views.StudentResultsView.as_view(), name='view_results'),
    path('semester/<int:semester_id>/', views.ResultDetailView.as_view(), name='semester_results'),
    path('download/<int:semester_id>/', views.download_result_pdf, name='download_pdf'),
    path('transcript/', views.download_transcript_pdf, name='download_transcript'),
]