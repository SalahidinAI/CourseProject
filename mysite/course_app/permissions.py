from rest_framework import permissions
from .models import Teacher, Student


class CheckStudentEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class CheckTeacherOrAdminEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.role == request.user.role


class CheckTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Teacher)


class CheckStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Student)


class CheckTeacherCourseEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not isinstance(request.user, Teacher):
            return False
        return obj.author.filter(id=request.user.id).exists()


class CheckTeacherLessonEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not isinstance(request.user, Teacher):
            return False
        return obj.course.author.filter(id=request.user.id).exists()


class CheckQuestionTeacherEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not isinstance(request.user, Teacher):
            return False
        return obj.exam.course.author.filter(id=request.user.id).exists()


class CheckOptionTeacherEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not isinstance(request.user, Teacher):
            return False
        return obj.question.exam.course.author.filter(id=request.user.id).exists()
