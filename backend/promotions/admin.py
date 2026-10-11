from django.contrib import admin

from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_type", "value", "applies_to", "valid_from", "valid_to", "is_active"]
    list_filter = ["is_active", "applies_to"]
    search_fields = ["code", "description"]
