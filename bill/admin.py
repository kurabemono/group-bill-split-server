from django.contrib import admin
from . import models


class BillItemInline(admin.StackedInline):
    model = models.BillItem


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = [BillItemInline]
    list_display = ['title', 'created_date']
    search_fields = ['title']


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
