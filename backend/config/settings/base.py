"""
Paramètres Django communs à tous les environnements.
SECRET_KEY et les credentials DB sont lus depuis l'environnement ;
une erreur explicite est levée en prod si SECRET_KEY est absente.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- Sécurité ----------------------------------------------------------------
# La valeur par défaut vide n'est utilisée qu'en dev ; base.py ne définit pas
# de fallback réel — chaque settings enfant gère la validation.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")

DEBUG = False  # toujours False par défaut ; dev.py le passe à True

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if h.strip()
]

# --- Applications ------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",        # requis par DRF pour l'authentification
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.health",
]

# --- Django REST Framework ---------------------------------------------------
REST_FRAMEWORK = {
    # Pas d'authentification ni de permission par défaut sur les endpoints publics
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

# --- Middleware ---------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

# --- Base de données ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "secondemand"),
        "USER": os.environ.get("POSTGRES_USER", "secondemand_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# --- Internationalisation -----------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Fichiers statiques ------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
