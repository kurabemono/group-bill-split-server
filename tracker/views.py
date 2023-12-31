from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .permissions import IsCreator, IsCreatorOrMember, IsCreatorOrMemberOfParentBill
from . import models, serializers


class BillViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsCreatorOrMember]
    search_fields = ['title']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateBillSerializer
        return serializers.BillSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Bill.objects.select_related('creator__user')

        member = models.Member.objects.only('id').get(user_id=user.id)
        creator_queryset = models.Bill.objects.filter(
            creator=member).select_related('creator__user')
        member_queryset = models.Bill.objects.filter(
            members=member).select_related('creator__user')
        return creator_queryset | member_queryset


class BillItemViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes.append(IsCreator)
        else:
            permission_classes.append(IsCreatorOrMemberOfParentBill)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddBillItemSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return serializers.UpdateBillItemSerializer

        return serializers.BillItemSerializer

    def get_serializer_context(self):
        return {'bill_id': self.kwargs['bill_pk']}

    def get_queryset(self):
        return models.BillItem.objects.filter(bill_id=self.kwargs['bill_pk'])
