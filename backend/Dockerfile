# ── Étape unique : image de production ──────────────────────────────────────
FROM python:3.14-slim

# Variables Python : pas de .pyc sur disque, logs non bufférisés (utile pour
# Docker), et PYTHONPATH pointe sur le répertoire de travail.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Installer les dépendances système minimales, puis nettoyer le cache apt
# dans la même couche pour réduire la taille de l'image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copier uniquement requirements.txt en premier pour profiter du cache Docker :
# la couche pip ne se reconstruit que si requirements.txt change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code applicatif.
COPY . .

# Créer un utilisateur non root dédié (UID 1001) et lui donner la propriété
# du répertoire de travail. Exécuter en non-root réduit la surface d'attaque
# en cas de faille applicative (pas de privilège pour écrire hors /app).
RUN adduser --system --no-create-home --uid 1001 appuser \
    && chown -R appuser /app
USER appuser

EXPOSE 8000

# gunicorn lie sur toutes les interfaces ; le nombre de workers est fixé à 2
# pour l'environnement de base (ajustable via variable d'environnement).
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
