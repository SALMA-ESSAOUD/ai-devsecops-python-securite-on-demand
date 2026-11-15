# SecOnDemand

## Conception et mise en œuvre d'une pipeline DevSecOps augmentée par IA pour les applications de l'écosystème Python (FastAPI, Django, Flask, …)

Plateforme web et mobile de vente de services de sécurité à la demande : pentest, SOC, audit cloud, analyse de vulnérabilités. Paiement Stripe (mode test). Pipeline DevSecOps augmentée par l'IA.

**Stack :** Django · Django REST Framework · PostgreSQL · React (Vite + TypeScript) · React Native · Docker · GitHub Actions · Terraform

---

## Structure du dépôt

```
ai-devsecops-python-securite-on-demand/
├── backend/          # API Django + DRF
├── web/              # Front-end React (Vite + TypeScript)
├── mobile/           # Application React Native
├── infra/            # Infrastructure as Code (Terraform)
├── docs/
│   └── threat-model/ # Modèle de menaces (T01–T50)
└── .github/
    └── workflows/    # Pipelines CI/CD GitHub Actions
```

---

## Commandes de démarrage

### Prérequis

- Docker ≥ 24 et Docker Compose v2
- Copier `.env.example` en `.env` et renseigner les valeurs

```bash
cp .env.example .env
```

### Démarrer tous les services

```bash
docker compose up --build
```

L'application est accessible sur <http://localhost:8080>.

### Backend seul (développement)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py migrate
python manage.py runserver
```

### Front-end seul (développement)

```bash
cd web
npm install
npm run dev
```

### Tests backend

```bash
cd backend
pytest
```
