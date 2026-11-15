from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """Renvoie {"status": "ok"} — utilisée par les health-checks des orchestrateurs."""
    return Response({"status": "ok"})
