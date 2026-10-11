from django.core.exceptions import ValidationError
from django.db import models


class Order(models.Model):
    """An online order from the storefront."""

    NUMBER_PREFIX = "O-"

    class Fulfilment(models.TextChoices):
        DELIVERY = "delivery", "Delivery"
        PICKUP = "pickup", "In-store pickup"

    class Status(models.TextChoices):
        PLACED = "placed", "Placed"
        PAID = "paid", "Paid"
        PACKED = "packed", "Packed"
        SHIPPED = "shipped", "Shipped"
        COLLECTED = "collected", "Collected"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(
        "customers.Customer",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="orders",
        help_text="Empty for guest orders.",
    )
    contact_name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=30)
    contact_email = models.EmailField()
    fulfilment = models.CharField(max_length=10, choices=Fulfilment.choices)
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    district = models.ForeignKey(
        "delivery.District", null=True, blank=True, on_delete=models.PROTECT, related_name="orders"
    )
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.ForeignKey(
        "delivery.Country", null=True, blank=True, on_delete=models.PROTECT, related_name="orders"
    )
    delivery_fee_lkr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    discount_lkr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    promotion = models.ForeignKey(
        "promotions.Promotion", null=True, blank=True, on_delete=models.PROTECT, related_name="orders"
    )
    total_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    display_currency = models.CharField(
        max_length=3, default="LKR", help_text="The currency the customer chose to view prices in."
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PLACED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number

    def clean(self):
        if self.fulfilment != self.Fulfilment.DELIVERY:
            return
        required = {
            "address_line1": self.address_line1,
            "city": self.city,
            "district": self.district_id,
            "country": self.country_id,
        }
        missing = [field for field, value in required.items() if not value]
        if missing:
            raise ValidationError({field: "Required for delivery." for field in missing})

    def save(self, *args, **kwargs):
        if not self.order_number:
            count = Order.objects.count() + 1
            self.order_number = f"{self.NUMBER_PREFIX}{count:04d}"
        super().save(*args, **kwargs)


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.PROTECT, related_name="+")
    quantity = models.PositiveIntegerField()
    # Copied at order time, so later price changes don't alter old orders.
    unit_price_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    line_total_lkr = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.variant}"
