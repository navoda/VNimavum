from django.db import IntegrityError
from django.test import TestCase

from sales.models import Sale
from services.models import ServiceOrder, ServiceType

from .models import Payment


class PaymentTargetTests(TestCase):
    def setUp(self):
        self.sale = Sale.objects.create(subtotal_lkr=5000, total_lkr=5000)
        self.job = ServiceOrder.objects.create(
            service_type=ServiceType.objects.create(name="Curtain sewing"),
            customer_name="Nimal",
            customer_phone="0771234567",
            price_lkr=3000,
        )

    def test_payment_for_a_sale(self):
        payment = Payment.objects.create(sale=self.sale, method="cash", amount_lkr=5000)
        self.assertEqual(payment.kind, "payment")

    def test_advance_and_balance_for_a_sewing_job(self):
        Payment.objects.create(service_order=self.job, method="cash", amount_lkr=1000)
        Payment.objects.create(service_order=self.job, method="bank_transfer", amount_lkr=2000, reference="88213")
        self.assertEqual(self.job.payments.count(), 2)

    def test_payment_must_belong_to_something(self):
        with self.assertRaises(IntegrityError):
            Payment.objects.create(method="cash", amount_lkr=100)

    def test_payment_cannot_belong_to_two_things(self):
        with self.assertRaises(IntegrityError):
            Payment.objects.create(sale=self.sale, service_order=self.job, method="cash", amount_lkr=100)
