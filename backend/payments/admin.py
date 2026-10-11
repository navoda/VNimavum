from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["received_at", "kind", "method", "amount_lkr", "status", "reference", "sale", "order", "service_order"]
    list_filter = ["kind", "method", "status"]
    search_fields = ["reference"]
    raw_id_fields = ["sale", "order", "service_order"]
