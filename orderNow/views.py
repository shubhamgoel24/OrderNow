"""
Views Module
"""

from django.http import JsonResponse
from rest_framework import status


def error_404(request, exception):
    return JsonResponse(
        {"status": "error", "data": None, "message": "URL Not Found."}, status=status.HTTP_404_NOT_FOUND
    )


def error_500(request):
    return JsonResponse(
        {"status": "error", "data": None, "message": "Internal Server Error"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
