from django.conf import settings
from django.db import models


class Customer(models.Model):
    """A registered customer. Guests have no row here."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer"
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=50, blank=True, help_text="For example Home or Work.")
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    district = models.ForeignKey(
        "delivery.District", null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.ForeignKey("delivery.Country", on_delete=models.PROTECT, related_name="+")

    class Meta:
        verbose_name_plural = "customer addresses"

    def __str__(self):
        return f"{self.label or 'Address'}: {self.address_line1}, {self.city}"
