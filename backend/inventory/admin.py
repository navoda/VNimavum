from django.contrib import admin

from .models import StockAlert, StockMovement


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["created_at", "variant", "quantity", "reason", "unit_cost_lkr", "note"]
    list_filter = ["reason"]
    search_fields = ["variant__sku", "variant__product__name", "note"]
    autocomplete_fields = ["variant"]
    raw_id_fields = ["sale", "order", "service_order"]


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ["created_at", "variant", "order", "read_at"]
