from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from . import models, serializers


class BillViewSet(ModelViewSet):
    queryset = models.Bill.objects.prefetch_related('items')
    serializer_class = serializers.BillSerializer
    search_fields = ['title']


class BillItemViewSet(ModelViewSet):
    pass
