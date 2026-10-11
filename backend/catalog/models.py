from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["sort_order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["parent", "name"], name="unique_category_name_per_parent"),
        ]

    def __str__(self):
        return f"{self.parent} > {self.name}" if self.parent else self.name

    def available_sizes(self):
        """Sizes for products in this category.

        A subcategory uses its parent's sizes unless it defines its own.
        """
        category = self
        while category is not None:
            sizes = category.sizes.all()
            if sizes.exists():
                return sizes
            category = category.parent
        return SizeOption.objects.none()


class SizeOption(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sizes")
    name = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "sort_order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["category", "name"], name="unique_size_name_per_category"),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    SKU_PREFIX = "VN-"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=20, unique=True, null=True, blank=True, editable=False)
    size = models.ForeignKey(
        SizeOption,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="variants",
    )
    colour_pattern = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    price_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["product", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "size", "colour_pattern", "material"],
                nulls_distinct=False,
                name="unique_variant_options_per_product",
            ),
        ]

    def __str__(self):
        options = [str(o) for o in (self.size, self.colour_pattern, self.material) if o]
        label = f"{self.product} ({', '.join(options)})" if options else str(self.product)
        return f"{self.sku} {label}" if self.sku else label

    def save(self, *args, **kwargs):
        # The SKU is built from the row's own ID (VN-00001), so it needs a
        # first save to get that ID.
        super().save(*args, **kwargs)
        if not self.sku:
            self.sku = f"{self.SKU_PREFIX}{self.pk:05d}"
            super().save(update_fields=["sku"])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    variant = models.ForeignKey(
        ProductVariant,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["product", "sort_order", "id"]

    def __str__(self):
        return f"Image {self.pk} of {self.product}"
