from django.contrib import admin

from .models import Customer, CustomerAddress


class CustomerAddressInline(admin.StackedInline):
    model = CustomerAddress
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "created_at"]
    search_fields = ["name", "email", "phone"]
    inlines = [CustomerAddressInline]
