from django.contrib import admin

from .models import CashSession, Sale, SaleLine


class SaleLineInline(admin.TabularInline):
    model = SaleLine
    extra = 0
    autocomplete_fields = ["variant"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "created_at", "total_lkr", "promotion"]
    search_fields = ["receipt_number", "receipt_email"]
    inlines = [SaleLineInline]


@admin.register(CashSession)
class CashSessionAdmin(admin.ModelAdmin):
    list_display = ["date", "opening_cash_lkr", "counted_cash_lkr", "closed_at"]
