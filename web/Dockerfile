# ── Étape 1 : build ─────────────────────────────────────────────────────────
FROM node:22-alpine AS builder

WORKDIR /app

# Copier les manifestes de dépendances en premier (cache Docker).
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

# Copier le reste du code et construire.
COPY . .
RUN npm run build

# ── Étape 2 : image de production (nginx non root) ───────────────────────────
# nginx:1.27-alpine inclut un utilisateur "nginx" (UID 101) précréé.
# On reconfigure nginx pour écouter sur le port 8080 (> 1024) afin de
# pouvoir lancer le processus sans privilèges root.
FROM nginx:1.27-alpine AS production

# Supprimer la configuration nginx par défaut.
RUN rm /etc/nginx/conf.d/default.conf

# Configuration nginx adaptée : port 8080, non root, logs vers stdout/stderr.
COPY nginx.conf /etc/nginx/conf.d/app.conf

# Copier les fichiers statiques buildés.
COPY --from=builder /app/dist /usr/share/nginx/html

# Ajuster les droits pour l'utilisateur nginx (UID 101).
RUN chown -R nginx:nginx /usr/share/nginx/html \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /var/log/nginx \
    && touch /var/run/nginx.pid \
    && chown nginx:nginx /var/run/nginx.pid

USER nginx

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
