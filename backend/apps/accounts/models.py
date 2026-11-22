"""
Modèle Utilisateur de la plateforme (tâche 1.1).

Contrat d'interface (voir le document « Organisation du travail ») :
- AUTH_USER_MODEL = "accounts.User", défini dès la première migration ;
- clé primaire UUID (identifiants non énumérables, menace T07) ;
- email unique, stocké en minuscules (menace T04 : pas de doublons par la casse) ;
- rôle : client ou admin (EF-04) ;
- aucun secret ni donnée sensible renvoyé par défaut : le secret TOTP
  est ajouté avec le chiffrement en tâche 2.7, pas ici.
"""
import uuid
from typing import ClassVar

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class Role(models.TextChoices):
    CLIENT = "client", "Client"
    ADMIN = "admin", "Administrateur"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email or not str(email).strip():
            raise ValueError("L'adresse électronique est obligatoire.")
        user = self.model(email=str(email).strip().lower(), **extra_fields)
        # password=None => mot de passe inutilisable (jamais de valeur en clair).
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", Role.CLIENT)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields["role"] = Role.ADMIN
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CLIENT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    def save(self, *args, **kwargs):
        # Normalisation unique : l'email est toujours comparé en minuscules.
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    def __str__(self):
        return self.email
