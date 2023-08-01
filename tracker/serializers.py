from rest_framework import serializers
from . import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = ['code', 'name', 'decimals']


class BillItemSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = models.BillItem
        fields = ['id', 'name', 'price', 'currency', 'paid_date', 'payer']


class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Bill
        fields = ['id', 'title', 'creator', 'members', 'items']
