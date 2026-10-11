from django.db import models
from django.db.models import Q


class Promotion(models.Model):
    """A discount code for in-store sales, online orders or both.

    There are no manual discounts at checkout; the owner applies a default code
    instead.
    """

    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percent"
        FIXED = "fixed", "Fixed amount (LKR)"

    class AppliesTo(models.TextChoices):
        IN_STORE = "in_store", "In store"
        ONLINE = "online", "Online"
        BOTH = "both", "Both"

    code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    applies_to = models.CharField(max_length=10, choices=AppliesTo.choices, default=AppliesTo.BOTH)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.CheckConstraint(condition=Q(value__gt=0), name="promotion_value_positive"),
            models.CheckConstraint(
                condition=~Q(discount_type="percent") | Q(value__lte=100),
                name="promotion_percent_at_most_100",
            ),
        ]

    def __str__(self):
        return self.code
