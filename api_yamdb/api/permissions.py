from rest_framework import permissions
from reviews.models import UserRole


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == UserRole.ADMIN


class AuthorOrModeratorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author
                or request.user.is_moderator_or_admin)


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or request.user == obj.author):
            return True
        return request.user.role in (UserRole.MODERATOR, UserRole.ADMIN)


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return request.user.role == UserRole.ADMIN

    def has_object_permission(self, request, obj, view):
        if request.method == 'GET' or request.user.role == UserRole.ADMIN:
            return True
        return False
