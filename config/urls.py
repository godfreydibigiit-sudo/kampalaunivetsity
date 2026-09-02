"""
Main URL configuration for KIU Result Management System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import UserLoginView

urlpatterns = [
    # Root URL - Directly show login page
    path('', UserLoginView.as_view(), name='login'),
    
    # Django Admin - Only at /admin/
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('apps.accounts.urls')),
    
    # Student Dashboard
    path('student/', include('apps.students.urls')),
    
    # Results
    path('results/', include('apps.results.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site
admin.site.site_header = "KIU Result Management System"
admin.site.site_title = "KIU Results Admin"
admin.site.index_title = "Welcome to KIU Results Management"