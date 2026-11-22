"""Tests du modèle Utilisateur (tâche 1.1)."""
import uuid

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError, transaction

from apps.accounts.models import Role, User

pytestmark = pytest.mark.django_db


def test_auth_user_model_is_accounts_user():
    assert settings.AUTH_USER_MODEL == "accounts.User"
    assert get_user_model() is User


def test_create_user_defaults():
    user = User.objects.create_user("client@example.com", "S3cret-pass-phrase")
    assert isinstance(user.pk, uuid.UUID)
    assert user.role == Role.CLIENT
    assert user.is_active is True
    assert user.is_admin is False
    assert user.created_at is not None
    assert str(user) == "client@example.com"


def test_password_is_hashed_never_stored_in_clear():
    user = User.objects.create_user("a@example.com", "S3cret-pass-phrase")
    user.refresh_from_db()
    assert user.password != "S3cret-pass-phrase"
    assert "S3cret-pass-phrase" not in user.password
    assert user.check_password("S3cret-pass-phrase")
    assert not user.check_password("autre-mot-de-passe")


def test_create_user_without_password_is_unusable():
    user = User.objects.create_user("nopass@example.com")
    assert not user.has_usable_password()


def test_email_is_normalized_to_lowercase():
    user = User.objects.create_user("  Hind.Test@Example.COM ", "S3cret-pass-phrase")
    assert user.email == "hind.test@example.com"


def test_email_is_required():
    with pytest.raises(ValueError):
        User.objects.create_user("", "S3cret-pass-phrase")
    with pytest.raises(ValueError):
        User.objects.create_user("   ", "S3cret-pass-phrase")


def test_email_unique_regardless_of_case():
    """Menace T04 : « A@x.com » et « a@x.com » ne sont pas deux comptes."""
    User.objects.create_user("dup@example.com", "S3cret-pass-phrase")
    with pytest.raises(IntegrityError), transaction.atomic():
        User.objects.create_user("DUP@example.com", "S3cret-pass-phrase")


def test_create_superuser_is_admin():
    admin = User.objects.create_superuser("admin@example.com", "S3cret-pass-phrase")
    assert admin.role == Role.ADMIN
    assert admin.is_admin is True


def test_create_user_cannot_be_made_admin_by_default():
    user = User.objects.create_user("c@example.com", "S3cret-pass-phrase")
    assert user.role == Role.CLIENT


def test_ids_are_unique_uuids():
    u1 = User.objects.create_user("u1@example.com", "S3cret-pass-phrase")
    u2 = User.objects.create_user("u2@example.com", "S3cret-pass-phrase")
    assert u1.pk != u2.pk


def test_no_pending_migrations():
    """Garde-fou : le modèle et la migration 0001 restent synchronisés."""
    call_command("makemigrations", "--check", "--dry-run", verbosity=0)
