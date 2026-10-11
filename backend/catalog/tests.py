from django.db import IntegrityError
from django.test import TestCase

from .models import Category, Product, ProductVariant, SizeOption


class CategorySizesTests(TestCase):
    def setUp(self):
        self.bedding = Category.objects.create(name="Bedding")
        self.single = SizeOption.objects.create(category=self.bedding, name="Single")
        self.king = SizeOption.objects.create(category=self.bedding, name="King")

    def test_subcategory_uses_parent_sizes(self):
        bedsheets = Category.objects.create(name="Bedsheets", parent=self.bedding)
        self.assertEqual(list(bedsheets.available_sizes()), [self.king, self.single])

    def test_subcategory_own_sizes_win(self):
        pillows = Category.objects.create(name="Pillows", parent=self.bedding)
        standard = SizeOption.objects.create(category=pillows, name="Standard")
        self.assertEqual(list(pillows.available_sizes()), [standard])

    def test_no_sizes_anywhere(self):
        candles = Category.objects.create(name="Candles")
        self.assertEqual(list(candles.available_sizes()), [])


class ProductVariantTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Bedsheets")
        self.queen = SizeOption.objects.create(category=category, name="Queen")
        self.product = Product.objects.create(category=category, name="Cotton bedsheet")

    def test_sku_is_generated_from_id(self):
        variant = ProductVariant.objects.create(product=self.product, size=self.queen, price_lkr=4500)
        self.assertEqual(variant.sku, f"VN-{variant.pk:05d}")
        variant.refresh_from_db()
        self.assertEqual(variant.sku, f"VN-{variant.pk:05d}")

    def test_same_options_twice_is_rejected(self):
        ProductVariant.objects.create(product=self.product, size=self.queen, colour_pattern="White", price_lkr=4500)
        with self.assertRaises(IntegrityError):
            ProductVariant.objects.create(
                product=self.product, size=self.queen, colour_pattern="White", price_lkr=4800
            )

    def test_same_options_without_size_twice_is_rejected(self):
        ProductVariant.objects.create(product=self.product, colour_pattern="Blue", price_lkr=1000)
        with self.assertRaises(IntegrityError):
            ProductVariant.objects.create(product=self.product, colour_pattern="Blue", price_lkr=1000)
