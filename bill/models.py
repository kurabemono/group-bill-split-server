from django.conf import settings
from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    decimals = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'currencies'


class Bill(models.Model):
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    display_currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_bills')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='participating_bills')


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField()
    payer = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)