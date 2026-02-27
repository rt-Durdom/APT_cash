from rest_framework import permissions

from .models import Collect, Payment


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Collect):
            return obj.author == request.user

        if isinstance(obj, Payment):
            return obj.donor == request.user

        return False
