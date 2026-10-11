from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text="ISO currency code, for example LKR.")
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "currencies"
        ordering = ["code"]

    def __str__(self):
        return self.code


class ExchangeRate(models.Model):
    """How many units of a currency one LKR buys on a given day."""

    class Source(models.TextChoices):
        FRANKFURTER = "frankfurter", "Frankfurter"
        MANUAL = "manual", "Manual"

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="rates")
    rate = models.DecimalField(max_digits=18, decimal_places=8, help_text="1 LKR = rate units.")
    date = models.DateField()
    source = models.CharField(max_length=12, choices=Source.choices)

    class Meta:
        ordering = ["-date", "currency"]
        constraints = [
            models.UniqueConstraint(
                fields=["currency", "date", "source"], name="unique_rate_per_currency_day_source"
            ),
        ]

    def __str__(self):
        return f"1 LKR = {self.rate} {self.currency} on {self.date}"

    @staticmethod
    def current(currency):
        """Latest rate for a currency. A manual rate wins over a downloaded one on the same day."""
        return (
            ExchangeRate.objects.filter(currency=currency)
            .order_by("-date", models.Case(
                models.When(source=ExchangeRate.Source.MANUAL, then=0), default=1
            ))
            .first()
        )
