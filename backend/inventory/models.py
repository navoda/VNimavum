import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q, Sum
from django.utils import timezone


class StockMovement(models.Model):
    """One change to the stock of a variant.

    The current stock count is the sum of all movements for that variant, so
    offline in-store sales and online orders merge without overwriting each
    other.
    """

    class Reason(models.TextChoices):
        RECEIVED = "received", "Received"
        SOLD_IN_STORE = "sold_in_store", "Sold in store"
        SOLD_ONLINE = "sold_online", "Sold online"
        RETURNED = "returned", "Returned"
        DAMAGED = "damaged", "Damaged"
        COUNT_CORRECTION = "count_correction", "Count correction"
        USED_IN_SEWING_JOB = "used_in_sewing_job", "Used in sewing job"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(
        "catalog.ProductVariant", on_delete=models.PROTECT, related_name="stock_movements"
    )
    quantity = models.IntegerField(help_text="Positive for stock in, negative for stock out.")
    reason = models.CharField(max_length=30, choices=Reason.choices)
    unit_cost_lkr = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Buying price per unit. Required when stock is received.",
    )
    sale = models.ForeignKey(
        "sales.Sale", null=True, blank=True, on_delete=models.PROTECT, related_name="stock_movements"
    )
    order = models.ForeignKey(
        "orders.Order", null=True, blank=True, on_delete=models.PROTECT, related_name="stock_movements"
    )
    service_order = models.ForeignKey(
        "services.ServiceOrder",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="stock_movements",
    )
    note = models.CharField(max_length=255, blank=True)
    # Set by the device that made the change, which may have been offline.
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(condition=~Q(quantity=0), name="stock_movement_quantity_not_zero"),
            models.CheckConstraint(
                condition=~Q(reason="received") | Q(unit_cost_lkr__isnull=False),
                name="stock_movement_received_has_unit_cost",
            ),
        ]

    def __str__(self):
        return f"{self.quantity:+d} {self.variant} ({self.get_reason_display()})"

    @staticmethod
    def stock_level(variant):
        """Current stock count for a variant."""
        total = StockMovement.objects.filter(variant=variant).aggregate(total=Sum("quantity"))["total"]
        return total or 0


class StockAlert(models.Model):
    """Raised when the last unit of a variant sells online."""

    variant = models.ForeignKey(
        "catalog.ProductVariant", on_delete=models.CASCADE, related_name="stock_alerts"
    )
    order = models.ForeignKey(
        "orders.Order", null=True, blank=True, on_delete=models.SET_NULL, related_name="stock_alerts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Last unit sold: {self.variant}"
