import uuid

from django.db import models
from django.utils import timezone


class Sale(models.Model):
    """One in-store sale, rung up by the owner at the counter."""

    RECEIPT_PREFIX = "S-"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt_number = models.CharField(max_length=20, unique=True, blank=True)
    subtotal_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    discount_lkr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    promotion = models.ForeignKey(
        "promotions.Promotion", null=True, blank=True, on_delete=models.PROTECT, related_name="sales"
    )
    total_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    receipt_email = models.EmailField(blank=True)
    # Set by the shop PC, which may have been offline.
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.receipt_number

    def save(self, *args, **kwargs):
        # The shop PC normally sends its own receipt number. This fills one in
        # for sales entered on the server, for example through the admin.
        if not self.receipt_number:
            count = Sale.objects.count() + 1
            self.receipt_number = f"{self.RECEIPT_PREFIX}{count:04d}"
        super().save(*args, **kwargs)


class SaleLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="lines")
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.PROTECT, related_name="+")
    quantity = models.PositiveIntegerField()
    # Copied at sale time, so later price changes don't alter old receipts.
    unit_price_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    line_total_lkr = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.variant}"


class CashSession(models.Model):
    """Optional opening and closing cash count for one day."""

    date = models.DateField(unique=True)
    opening_cash_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    counted_cash_lkr = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    opened_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Cash for {self.date}"
