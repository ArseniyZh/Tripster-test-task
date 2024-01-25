from rest_framework import permissions


class PublicationBelongToUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Принадлежит ли публикация пользователю
        """
        return obj.author == request.user


class VoteBelongToUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Принадлежит ли голос пользователю
        """
        return obj.user == request.user
