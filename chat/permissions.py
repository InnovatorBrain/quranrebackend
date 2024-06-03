from rest_framework.permissions import BasePermission

class IsTeacherOrStudent(BasePermission):
    """
    Custom permission to only allow teachers or students to access the chat.
    """
    def has_permission(self, request, view):
        return request.user.is_teacher or request.user.is_student
