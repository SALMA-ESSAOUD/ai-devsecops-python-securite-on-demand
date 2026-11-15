# SecOnDemand

> **Conception et mise en œuvre d'une pipeline DevSecOps augmentée par l'IA pour les applications de l'écosystème Python**
>
> Projet 5 — Module « Sécurité des applications et des services »
> Cycle ingénieur SIT 3 · Université Cadi Ayyad (UCA) · FST Marrakech · 2026/2027
>
> Équipe : Hind Zabrati · Imane Arrach · Salma Essaoud · Salma Bender

---

## Présentation

**SecOnDemand** est une plateforme web et mobile de vente de services de cybersécurité à la demande : test d'intrusion, surveillance SOC, audit de configuration cloud et analyse de vulnérabilités. Les paiements sont simulés via l'API Stripe en mode test — aucune donnée bancaire réelle n'est traitée.

L'application sert de support démonstratif à une **pipeline DevSecOps augmentée par l'IA**, qui met en œuvre les onze pratiques Tier 1 définies par Prates & Pereira (2025) et les référentiels OWASP Top 10 : 2025, API Security Top 10, Mobile Top 10 et Top 10 for LLM Applications.

---

## Stack technique

| Couche | Technologie |
|---|---|
| API REST | Django 5.2 LTS · Django REST Framework 3.18 |
| Base de données | PostgreSQL 17 |
| Front-end web | React 19 · Vite 8 · TypeScript 7 |
| Application mobile | React Native (à venir) |
| Reverse proxy | nginx 1.27 |
| Conteneurisation | Docker · Docker Compose v2 |
| CI/CD | GitHub Actions (actions épinglées par SHA) |
| Infrastructure as Code | Terraform (à venir) |
| Qualité Python | ruff · pytest · pytest-django |

---

## Architecture

```
                        ┌─────────────────────────────────────────┐
                        │              Internet (HTTPS)            │
                        └──────────────┬──────────────────────────┘
                                       │ :8080
                               ┌───────▼────────┐
                               │  nginx (proxy) │  X-Content-Type-Options
                               │                │  X-Frame-Options
                               └──┬─────────┬───┘  Referrer-Policy
                      /api/        │         │        /
               ┌──────▼──────┐    │    ┌────▼──────────┐
               │   Backend   │    │    │   Front-end   │
               │  Django +   │    │    │  React (Vite) │
               │    DRF      │    │    └───────────────┘
               └──────┬──────┘    │
                      │           │  Réseau interne (backend_net)
               ┌──────▼──────┐
               │ PostgreSQL  │  ← aucun port exposé à l'hôte
               └─────────────┘
```

**Trois modules métier :**
- **Comptes et accès** — inscription, authentification, rôles client / administrateur
- **Missions et rapports** — catalogue des prestations, suivi de l'état, téléchargement sécurisé
- **Paiements** — montant calculé côté serveur, webhooks Stripe signés, reçus

---

## Modèle de menaces

Le modèle de menaces (méthode STRIDE, v1.0) est versionné dans [`docs/threat-model/`](docs/threat-model/).
Il couvre **50 menaces** (3 critiques, 17 élevées, 28 modérées, 2 faibles) réparties sur neuf domaines :
authentification, contrôle d'accès, paiement, rapports, mobile, infrastructure, journalisation, pipeline CI/CD et IA.

Les trois menaces critiques — BOLA (T07), modification du montant (T17), bourrage d'identifiants (T01) — disposent chacune d'une contre-mesure vérifiée par un test automatisé bloquant en CI.

---

## Structure du dépôt

```
.
├── backend/                  # API Django + DRF
│   ├── apps/
│   │   └── health/           # GET /api/health/ → {"status": "ok"}
│   ├── config/
│   │   └── settings/
│   │       ├── base.py       # Paramètres communs
│   │       ├── dev.py        # Développement local
│   │       └── prod.py       # Production (SECRET_KEY obligatoire)
│   ├── tests/                # pytest
│   ├── Dockerfile            # Image python:3.14-slim, utilisateur non root
│   ├── requirements.txt      # Versions figées
│   └── ruff.toml             # Configuration du linter
├── web/                      # Front-end React (Vite + TypeScript)
│   ├── src/
│   │   ├── App.tsx           # Appel /api/health/, affichage du statut
│   │   └── main.tsx
│   ├── Dockerfile            # Build multi-étapes, nginx non root
│   └── nginx.conf            # Port 8080, SPA routing
├── mobile/                   # Application React Native (à venir)
├── infra/
│   └── nginx/
│       └── nginx.conf        # Reverse proxy + en-têtes de sécurité
├── docs/
│   └── threat-model/         # Modèle de menaces STRIDE (v1.0)
├── .github/
│   ├── workflows/
│   │   └── ci.yml            # Lint · Tests · Build Docker (SHA épinglés)
│   ├── CODEOWNERS            # Revue obligatoire : @SALMA-ESSAOUD
│   └── pull_request_template.md  # Checklist sécurité (T01–T50)
├── docker-compose.yml        # db · backend · web · nginx
├── .env.example              # Variables d'environnement (valeurs factices)
└── .gitignore
```

---

## Démarrage rapide

### Prérequis

- Docker ≥ 24 et Docker Compose v2
- Git

### 1 — Cloner et configurer l'environnement

```bash
git clone git@github.com:SALMA-ESSAOUD/ai-devsecops-python-securite-on-demand.git
cd ai-devsecops-python-securite-on-demand
cp .env.example .env
# Éditer .env et remplacer toutes les valeurs "changeme-"
```

### 2 — Démarrer tous les services

```bash
docker compose up --build
```

L'application est accessible sur **<http://localhost:8080>**.
L'endpoint de santé répond sur **<http://localhost:8080/api/health/>**.

### 3 — Développement backend (hors Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=config.settings.dev
# Pas de PostgreSQL local requis pour les tests unitaires
pytest
```

### 4 — Développement front-end (hors Docker)

```bash
cd web
npm install
npm run dev        # Proxy /api/ → http://localhost:8000 (Vite)
```

---

## Pipeline CI/CD

Le workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) se déclenche sur chaque `push` vers `main` et sur chaque `pull_request`.

| Job | Outil | Ce qui est vérifié |
|---|---|---|
| `lint` | ruff 0.17.5 | Style et erreurs statiques Python |
| `tests` | pytest + service PostgreSQL | Route `/api/health/`, non-régression |
| `docker-build` | docker/build-push-action | Build des images backend et web (sans push) |

**Règles de sécurité CI :**
- `pull_request_target` **jamais** utilisé
- `permissions: contents: read` au niveau workflow
- Chaque action épinglée par son SHA de commit complet (40 caractères)

---

## Sécurité — points clés

| Décision | Justification |
|---|---|
| `DEBUG=False` par défaut | Évite la fuite d'informations techniques en production (T15) |
| `SECRET_KEY` depuis l'environnement, erreur explicite si absente en prod | Empêche le démarrage silencieux avec une clé vide (T05) |
| Conteneurs non root (UID 1001 / 101) | Réduit la surface d'attaque en cas d'évasion (T34) |
| PostgreSQL sans port exposé à l'hôte | Interdit l'accès réseau direct à la base (T32) |
| Réseau Docker isolé `backend_net` | nginx et web ne peuvent pas joindre la DB directement |
| En-têtes HTTP : `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` | Défense en profondeur contre le sniffing MIME et le clickjacking (T36) |
| Actions CI épinglées par SHA | Protection contre les attaques supply-chain sur les workflows (T42) |
| `CODEOWNERS` + PR template | Revue humaine obligatoire, traçabilité vers le modèle de menaces (T43) |

---

## Contribuer

1. Créer une branche depuis `main`
2. Ouvrir une pull request — le template de PR s'affiche automatiquement
3. Remplir la **checklist de sécurité** et indiquer la menace concernée (T01–T50)
4. Le CI doit passer (lint + tests + build) avant tout merge
5. La revue de `@SALMA-ESSAOUD` est requise (CODEOWNERS)

---

## Licence

Projet universitaire — usage académique uniquement.
