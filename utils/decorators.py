from account.permission import get_user_permissions_new
from rest_framework import permissions
from utils.api_exceptions import (
    AlreadyLoginUserException,
    BlockedUserException,
    DeletedUserException,
    InactiveUserException,
    NotAllowedPastorException,
    NotMappedAsPastorException,
    UnverifiedUserException,
    UserNotActiveException,
    LoginRequiredException,
    UserPermissionDenied,
)


class ActiveUserPermission(permissions.BasePermission):
    """
    Required permission for active users
    """

    def has_permission(self, request, view):
        # print(request.META)
        if not request.user.is_anonymous:
            if request.user.is_active:
                return True
            raise UserNotActiveException
        raise LoginRequiredException


class AutUserAlreadyPermission(permissions.BasePermission):
    """
    Already Login user
    """

    def has_permission(self, request, view):
        # print(request.META)
        if not request.user.is_anonymous:
            if request.user.is_authenticated:
                raise AlreadyLoginUserException
        return True


class DisallowedUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_active:
            raise InactiveUserException
        if request.user.is_blocked:
            raise BlockedUserException
        if request.user.is_deleted:
            raise DeletedUserException
        if not request.user.is_verified:
            raise UnverifiedUserException
        if not hasattr(request.user, 'pastor_user'):
            raise NotMappedAsPastorException
        return True


class DisallowedNotAssemblyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user.user_type)
        if request.user.user_type not in ["Assembly_Pastor", "District_Pastor", "Area_Pastor", "Superintendent"]:
            raise NotAllowedPastorException
        required_permissions = ["assembly_admin", "district_admin", "area_admin", "superintendent"]
        user_perms = get_user_permissions_new(request.user)
        if not any(perm in user_perms for perm in required_permissions):
            raise UserPermissionDenied
        return True


class DisallowedNotPastorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user.user_type)
        if request.user.user_type not in ["Student_pastor", "Full_Pastor", "Assembly_Pastor", "District_Pastor", "Area_Pastor", "Superintendent"]:
            raise NotAllowedPastorException
        return True


class DisallowedNotAllowedUserTypePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user.user_type)
        if request.user.user_type not in ["Assistance_admin", "Student_pastor", "Full_Pastor", "Assembly_Pastor", "District_Pastor", "Area_Pastor", "Superintendent"]:
            raise NotAllowedPastorException
        return True
