from django.db import IntegrityError
from django.test import TestCase

from catalog.models import Category, Product, ProductVariant

from .models import StockMovement


class StockLevelTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Cushions")
        product = Product.objects.create(category=category, name="Linen cushion")
        self.variant = ProductVariant.objects.create(product=product, price_lkr=2500)

    def test_stock_is_sum_of_movements(self):
        StockMovement.objects.create(variant=self.variant, quantity=20, reason="received", unit_cost_lkr=1200)
        StockMovement.objects.create(variant=self.variant, quantity=-1, reason="sold_in_store")
        StockMovement.objects.create(variant=self.variant, quantity=-1, reason="sold_online")
        StockMovement.objects.create(variant=self.variant, quantity=-2, reason="damaged")
        self.assertEqual(StockMovement.stock_level(self.variant), 16)

    def test_no_movements_means_zero(self):
        self.assertEqual(StockMovement.stock_level(self.variant), 0)

    def test_received_needs_unit_cost(self):
        with self.assertRaises(IntegrityError):
            StockMovement.objects.create(variant=self.variant, quantity=5, reason="received")

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(IntegrityError):
            StockMovement.objects.create(variant=self.variant, quantity=0, reason="count_correction")
