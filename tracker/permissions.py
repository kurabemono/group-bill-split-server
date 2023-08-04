
from rest_framework import permissions
from .models import Bill


class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.member.id == obj.creator.id


class IsCreatorOrMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.member.id
        is_creator = obj.creator.id == user_id
        is_member = obj.members.filter(pk=user_id).exists()
        return is_creator or is_member


class IsCreatorOrMemberOfParentBill(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.member.id
        bill_id = view.kwargs.get('bill_pk')
        try:
            bill = Bill.objects.get(pk=bill_id)
            is_creator = bill.creator.pk == user_id
            is_member = bill.members.filter(pk=user_id).exists()
            return is_creator or is_member
        except Bill.DoesNotExist:
            return False

    # def has_object_permission(self, request, view, obj):
    #     user_id = request.user.member.id
    #     is_creator = obj.bill.creator.id == user_id
    #     is_member = obj.bill.members.filter(pk=user_id).exists()
    #     print(f'is_creator: {is_creator}')
    #     print(f'is_member: {is_member}')
    #     return is_creator or is_member
