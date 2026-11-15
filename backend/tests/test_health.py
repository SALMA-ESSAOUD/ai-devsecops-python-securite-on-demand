import pytest
from django.test import Client


@pytest.mark.django_db(databases=[])
def test_health_check_returns_ok():
    """
    GET /api/health/ doit renvoyer 200 avec {"status": "ok"}.
    databases=[] indique à pytest-django que ce test ne touche pas la DB,
    ce qui permet de l'exécuter sans connexion PostgreSQL (pratique en CI
    avant que le service DB soit prêt, et en développement local hors Docker).
    """
    client = Client()
    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
