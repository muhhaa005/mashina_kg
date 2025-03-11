from rest_framework import permissions

class CheckUserReview(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'client':
            return True
        return False