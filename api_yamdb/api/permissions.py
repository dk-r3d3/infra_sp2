"""High level support for doing this and that."""
from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    """High level support for doing this and that."""

    def has_permission(self, request, view):
        """High level support for doing this and that."""
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        """High level support for doing this and that."""
        return request.method in permissions.SAFE_METHODS


class IsModerator(permissions.BasePermission):
    """High level support for doing this and that."""

    def has_permission(self, request, view):
        """High level support for doing this and that."""
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        """High level support for doing this and that."""
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    """High level support for doing this and that."""

    def has_permission(self, request, view):
        """High level support for doing this and that."""
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        """High level support for doing this and that."""
        return request.user.is_authenticated and request.user.is_admin


class IsSuperuser(permissions.BasePermission):
    """High level support for doing this and that."""

    def has_permission(self, request, view):
        """High level support for doing this and that."""
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        """High level support for doing this and that."""
        return request.user and request.user.is_superuser


class IsAuthor(permissions.BasePermission):
    """High level support for doing this and that."""

    def has_object_permission(self, request, view, obj):
        """High level support for doing this and that."""
        return obj.author == request.user
