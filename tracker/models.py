from django.conf import settings
from django.contrib import admin
from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    decimals = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f'{self.code} - {self.name}'

    class Meta:
        verbose_name_plural = 'currencies'


class Member(models.Model):
    preferred_currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username}'

    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username


class Bill(models.Model):
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    display_currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    creator = models.ForeignKey(
        Member, on_delete=models.PROTECT, related_name='created_bills')
    members = models.ManyToManyField(
        Member, blank=True, related_name='participating_bills')

    def __str__(self) -> str:
        return self.title


class BillItem(models.Model):
    bill = models.ForeignKey(
        Bill, on_delete=models.CASCADE, related_name='items')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField()
    payer = models.ForeignKey(Member, on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)
