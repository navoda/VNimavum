from django.core.exceptions import ValidationError
from django.test import TestCase

from delivery.models import Country, District

from .models import Order


class OrderTests(TestCase):
    def order(self, **fields):
        return Order(
            contact_name="Kamala",
            contact_phone="0771234567",
            contact_email="kamala@example.com",
            subtotal_lkr=4500,
            total_lkr=4500,
            **fields,
        )

    def test_pickup_needs_no_address(self):
        order = self.order(fulfilment="pickup")
        order.full_clean()
        order.save()
        self.assertTrue(order.order_number.startswith("O-"))

    def test_delivery_needs_address(self):
        with self.assertRaises(ValidationError) as error:
            self.order(fulfilment="delivery").full_clean()
        self.assertEqual(
            set(error.exception.message_dict), {"address_line1", "city", "district", "country"}
        )

    def test_delivery_with_address(self):
        sri_lanka = Country.objects.get(code="LK")
        colombo = District.objects.get(country=sri_lanka, name="Colombo")
        self.order(
            fulfilment="delivery",
            address_line1="12 Galle Road",
            city="Colombo 3",
            district=colombo,
            country=sri_lanka,
        ).full_clean()

    def test_sri_lanka_districts_are_loaded(self):
        self.assertEqual(District.objects.filter(country__code="LK").count(), 25)
