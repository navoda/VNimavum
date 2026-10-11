from django.contrib import admin

from inventory.models import StockMovement

from .models import Category, Product, ProductImage, ProductVariant, SizeOption


class SizeOptionInline(admin.TabularInline):
    model = SizeOption
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["__str__", "is_active", "sort_order"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    inlines = [SizeOptionInline]


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ["sku", "size", "colour_pattern", "material", "price_lkr", "is_active"]
    readonly_fields = ["sku"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_active", "updated_at"]
    list_filter = ["is_active", "category"]
    search_fields = ["name", "variants__sku"]
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ["sku", "product", "size", "colour_pattern", "material", "price_lkr", "stock", "is_active"]
    list_filter = ["is_active", "product__category"]
    search_fields = ["sku", "product__name", "colour_pattern", "material"]
    readonly_fields = ["sku"]

    @admin.display(description="Stock")
    def stock(self, obj):
        return StockMovement.stock_level(obj)
