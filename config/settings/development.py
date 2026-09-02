"""
Development settings - No HTTPS issues
"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = [ "kampalauniversity.pythonanywhere.com",
    "localhost",
    "127.0.0.1",]

# NO SSL/HTTPS in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'