"""
Paramètres pour l'environnement de développement local.
DEBUG est activé et un fallback de SECRET_KEY est fourni pour le confort.
Ne jamais utiliser ce fichier en production.
"""
from .base import *  # noqa: F401, F403

DEBUG = True

# Fallback local uniquement — sans valeur en prod, prod.py lève une erreur.
if not SECRET_KEY:
    SECRET_KEY = "dev-only-insecure-secret-key-do-not-use-in-production"

if not ALLOWED_HOSTS:  # noqa: F405
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
