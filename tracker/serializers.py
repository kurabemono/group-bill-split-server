from rest_framework import serializers
from . import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = ['code', 'name', 'decimals']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ['id', 'username', 'preferred_currency']


class SimpleMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ['id', 'username']


class BillItemSerializer(serializers.ModelSerializer):
    # currency = CurrencySerializer()
    payer = SimpleMemberSerializer()

    class Meta:
        model = models.BillItem
        fields = ['id', 'name', 'price', 'currency', 'paid_date', 'payer']


class AddBillItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        bill_id = self.context['bill_id']
        return models.BillItem.objects.create(bill_id=bill_id, **validated_data)

    class Meta:
        model = models.BillItem
        fields = ['id', 'name', 'price', 'currency', 'paid_date', 'payer']


class BillSerializer(serializers.ModelSerializer):
    creator = SimpleMemberSerializer()

    class Meta:
        model = models.Bill
        fields = ['id', 'title', 'creator', 'members']


class CreateBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bill
        fields = ['id', 'title', 'creator', 'members']
