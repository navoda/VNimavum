from django.contrib import admin

from .models import ServiceOrder, ServiceType


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "default_price_lkr", "is_active"]


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ["job_number", "customer_name", "service_type", "price_lkr", "due_date", "status"]
    list_filter = ["status", "service_type"]
    search_fields = ["job_number", "customer_name", "customer_phone"]
