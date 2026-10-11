import uuid

from django.db import models
from django.db.models import Q
from django.utils import timezone


class Payment(models.Model):
    """Money in or out for a sale, an online order or a sewing job."""

    class Kind(models.TextChoices):
        PAYMENT = "payment", "Payment"
        REFUND = "refund", "Refund"

    class Method(models.TextChoices):
        CASH = "cash", "Cash"
        BANK_TRANSFER = "bank_transfer", "Bank transfer"
        CARD = "card", "Card"
        PAYPAL = "paypal", "PayPal"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(
        "sales.Sale", null=True, blank=True, on_delete=models.PROTECT, related_name="payments"
    )
    order = models.ForeignKey(
        "orders.Order", null=True, blank=True, on_delete=models.PROTECT, related_name="payments"
    )
    service_order = models.ForeignKey(
        "services.ServiceOrder",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="payments",
    )
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.PAYMENT)
    method = models.CharField(max_length=20, choices=Method.choices)
    amount_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(
        max_length=100, blank=True, help_text="Bank transfer reference or payment provider ID."
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.COMPLETED)
    # Set by the device that took the payment, which may have been offline.
    received_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-received_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(sale__isnull=False, order__isnull=True, service_order__isnull=True)
                    | Q(sale__isnull=True, order__isnull=False, service_order__isnull=True)
                    | Q(sale__isnull=True, order__isnull=True, service_order__isnull=False)
                ),
                name="payment_for_exactly_one_thing",
            ),
            models.CheckConstraint(condition=Q(amount_lkr__gt=0), name="payment_amount_positive"),
        ]

    def __str__(self):
        return f"{self.get_kind_display()} {self.amount_lkr} LKR ({self.get_method_display()})"
