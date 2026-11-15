## Description

<!-- Décrivez brièvement les changements apportés par cette PR. -->

## Checklist de sécurité

- [ ] **Autorisation par objet vérifiée** — chaque accès à une ressource contrôle que l'utilisateur courant en est bien le propriétaire ou y a droit (prévention IDOR).
- [ ] **Aucun secret dans le code** — aucune clé API, mot de passe, token ou valeur sensible commité ; toutes les valeurs sensibles passent par des variables d'environnement ou un vault.
- [ ] **Tests ajoutés ou mis à jour** — la fonctionnalité ou le correctif est couvert par au moins un test automatisé.
- [ ] **Entrées validées** — toutes les données reçues de l'extérieur (HTTP, fichiers, CLI) sont validées et assainies avant utilisation.
- [ ] **Dépendances vérifiées** — toute nouvelle dépendance a été examinée (licence, maintenabilité, absence d'alerte CVE connue).
- [ ] **Lien vers la menace concernée** — indiquer ci-dessous l'identifiant de la menace du modèle de menaces si cette PR la traite ou la modifie.

## Menace(s) du modèle de menaces concernée(s)

<!-- Indiquer l'identifiant (T01 à T50) et le titre court de la menace.
     Exemple : T07 — Injection SQL sur le endpoint /api/orders/ -->

- Menace : <!-- T__ — description -->

## Tests effectués

<!-- Décrire comment les changements ont été testés (commandes, cas limites couverts). -->
