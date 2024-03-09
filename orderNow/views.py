"""
Views Module
"""

from django.http import JsonResponse
from rest_framework import status


def error_404(request, exception):
    """
    Custom view for Not Found error
    """

    return JsonResponse(
        {"status": "error", "data": None, "message": "URL Not Found."}, status=status.HTTP_404_NOT_FOUND
    )


def error_500(request):
    """
    Custom view for Internal Server error
    """

    return JsonResponse(
        {"status": "error", "data": None, "message": "Internal Server Error"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
