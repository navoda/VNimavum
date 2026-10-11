from django.db import models
from django.db.models import F, Q


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True, help_text="ISO country code, for example LK.")
    name = models.CharField(max_length=100)
    delivery_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "countries"
        ordering = ["name"]

    def __str__(self):
        return self.name


class District(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="districts")
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False, help_text="Whether the shop delivers here.")
    delivery_fee_lkr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    est_days_min = models.PositiveIntegerField(null=True, blank=True)
    est_days_max = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["country", "name"]
        constraints = [
            models.UniqueConstraint(fields=["country", "name"], name="unique_district_per_country"),
            models.CheckConstraint(
                condition=Q(est_days_min__isnull=True)
                | Q(est_days_max__isnull=True)
                | Q(est_days_min__lte=F("est_days_max")),
                name="district_est_days_in_order",
            ),
        ]

    def __str__(self):
        return self.name
