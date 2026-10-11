import uuid

from django.db import models
from django.utils import timezone


class ServiceType(models.Model):
    """A kind of sewing job, for example curtain sewing or alterations."""

    name = models.CharField(max_length=100, unique=True)
    default_price_lkr = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceOrder(models.Model):
    """A sewing job where the customer brings their own material.

    Payments link to it like a sale: an optional advance plus the balance, or
    one payment at collection. Shop stock used on the job is recorded as stock
    movements.
    """

    NUMBER_PREFIX = "J-"

    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        IN_PROGRESS = "in_progress", "In progress"
        READY = "ready", "Ready"
        COLLECTED = "collected", "Collected"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_number = models.CharField(max_length=20, unique=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name="orders")
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=30)
    customer = models.ForeignKey(
        "customers.Customer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="service_orders",
    )
    description = models.TextField(blank=True)
    material_notes = models.TextField(blank=True, help_text="What the customer brought.")
    quantity = models.PositiveIntegerField(default=1)
    price_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.RECEIVED)
    # Set by the shop PC, which may have been offline.
    created_at = models.DateTimeField(default=timezone.now)
    collected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.job_number} {self.customer_name}"

    def save(self, *args, **kwargs):
        # The shop PC normally sends its own job number. This fills one in for
        # jobs entered on the server, for example through the admin.
        if not self.job_number:
            count = ServiceOrder.objects.count() + 1
            self.job_number = f"{self.NUMBER_PREFIX}{count:04d}"
        super().save(*args, **kwargs)
