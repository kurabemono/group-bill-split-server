from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.member.id == obj.creator


class IsOwnerOrMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.member.id
        print(obj)
        print(f'is_creator: {obj.creator_id == user_id}')
        print(f'is_owner: {obj.members.filter(pk=user_id).exists()}')
        return obj.creator_id == user_id or obj.members.filter(pk=user_id).exists()
