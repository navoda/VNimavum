from django.contrib import admin

from .models import Order, OrderLine


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    autocomplete_fields = ["variant"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "created_at", "contact_name", "fulfilment", "total_lkr", "status"]
    list_filter = ["status", "fulfilment"]
    search_fields = ["order_number", "contact_name", "contact_email", "contact_phone"]
    inlines = [OrderLineInline]
