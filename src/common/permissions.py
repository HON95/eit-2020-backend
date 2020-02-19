from rest_framework.permissions import BasePermission, SAFE_METHODS


class DenyAll(BasePermission):
    """Deny everything."""
    def has_permission(self, request, view):
        return False


class AllowAll(BasePermission):
    """Allow everything. Same as empty permission set."""
    def has_permission(self, request, view):
        return True


class IsSuperuser(BasePermission):
    """Allow if user is superuser."""
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsStaff(BasePermission):
    """Allow if user is staff."""
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    """Allow if user is owner of resource."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelf(BasePermission):
    """Allow if the user is the resource."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsReadOnly(BasePermission):
    """Allow if request is using a safe (read-only) HTTP method."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsActive(BasePermission):
    """
    Allow if the object is active.
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_active


class IsInactive(BasePermission):
    """
    Allow if the object is not active.
    """

    def has_object_permission(self, request, view, obj):
        return not obj.is_active


class StringPermission(BasePermission):
    """
    DRF permission wrapper for a model string permission, such as `seating.layout.list`.
    """

    def __init__(self, string_permission):
        if not isinstance(string_permission, str):
            raise TypeError("Model permission must be a string")
        self.string_permission = string_permission

    def has_permission(self, request, view):
        return request.user.has_perm(self.string_permission)


class ConjunctionPermission(BasePermission):
    """
    Create new permission as conjunction (AND) of provided instantiated permissions.
    Requires all permissions to have both `has_permission` and `has_object_permission` satisfied.
    """

    def __init__(self, *permissions):
        self.permissions = permissions

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        for permission in self.permissions:
            if not permission.has_permission(request, view) or not permission.has_object_permission(request, view, obj):
                return False
        return True


class DisjunctionPermission(BasePermission):
    """
    Create new permission as disjunction (OR) of provided instantiated permissions.
    Requires at least one permission to have both `has_permission` and `has_object_permission` satisfied.
    """

    def __init__(self, *permissions):
        self.permissions = permissions

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        for permission in self.permissions:
            if permission.has_permission(request, view) and permission.has_object_permission(request, view, obj):
                return True
        return False
