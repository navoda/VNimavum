from django.contrib import admin

from .models import Country, District


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "delivery_enabled"]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "is_available", "delivery_fee_lkr", "est_days_min", "est_days_max"]
    list_editable = ["is_available", "delivery_fee_lkr", "est_days_min", "est_days_max"]
    list_filter = ["is_available", "country"]
