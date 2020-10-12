from django.conf import settings

from rest_framework.permissions import BasePermission


class ApiKeyPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        api_key = request.META.get("HTTP_X_API_KEY", None)
        if api_key:
            return api_key in settings.ALLOWED_API_KEYS
        return False
