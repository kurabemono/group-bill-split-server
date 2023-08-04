from rest_framework import serializers, status
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
    creator = SimpleMemberSerializer()

    class Meta:
        model = models.BillItem
        fields = ['id', 'name', 'price', 'currency', 'paid_date', 'creator']


class AddBillItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        bill_id = self.context['bill_id']
        if not models.Bill.objects.filter(pk=bill_id).exists():
            print('Bill does not exist')
            raise serializers.ValidationError('Bill does not exist')
        return models.BillItem.objects.create(bill_id=bill_id, **validated_data)

    class Meta:
        model = models.BillItem
        fields = ['id', 'name', 'price', 'currency', 'paid_date', 'creator']


class UpdateBillItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BillItem
        fields = ['name', 'price', 'currency', 'paid_date']


class BillSerializer(serializers.ModelSerializer):
    creator = SimpleMemberSerializer()

    class Meta:
        model = models.Bill
        fields = ['id', 'title', 'creator', 'display_currency', 'members']


class CreateBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bill
        fields = ['id', 'title', 'creator', 'display_currency', 'members']
