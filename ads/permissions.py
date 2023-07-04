from rest_framework.permissions import BasePermission

from ads.models import UserRoles


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            owner = obj.owner
        elif hasattr(obj, 'author'):
            owner = obj.author
        else:
            raise Exception('Error')
        return owner == request.user


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]

