"""
Settings initialization - Simple version
"""
import os

# Default to development
DJANGO_ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if DJANGO_ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *