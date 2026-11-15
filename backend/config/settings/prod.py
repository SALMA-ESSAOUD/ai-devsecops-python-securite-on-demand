"""
Paramètres pour l'environnement de production.
SECRET_KEY doit être définie via la variable d'environnement DJANGO_SECRET_KEY ;
une ImproperlyConfigured est levée au démarrage si elle est absente ou vide.
"""
import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401, F403

# Validation stricte de SECRET_KEY en production
_secret = os.environ.get("DJANGO_SECRET_KEY", "")
if not _secret:
    raise ImproperlyConfigured(
        "La variable d'environnement DJANGO_SECRET_KEY est absente ou vide. "
        "Définissez-la avant de démarrer l'application en production."
    )
SECRET_KEY = _secret  # noqa: F405

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
