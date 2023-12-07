from django.test import TestCase
from django.utils import timezone
from vendor_app.models import Vendor,PurchaseOrder
from datetime import timedelta
from django.db.models import Sum


class PurchaseOrderTestCase(TestCase):
    def setUp(self):
        # Create a Vendor for testing
        self.vendor = Vendor.objects.create(name='Test Vendor',
                                            contact_details="Test Contact Details",
                                            address="Test Address",
                                            vendor_code="TEST123")

        # Create a PurchaseOrder instance for testing
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=7),
            items=[{"item_code": "ITEM-1", "description": "Product X", "quantity": 5}],
            quantity=5,
            status='pending',
            quality_rating=None,
            issue_date=timezone.now(),
            acknowledgment_date=None,
        )

    def tearDown(self):
        self.vendor.delete()
        self.purchase_order.delete()

    def test_purchase_order_str_method(self):
        self.assertEqual(
            str(self.purchase_order),
            f"PO#PO123 for {self.vendor}"
        )

    def test_purchase_order_data(self):
        self.assertEqual(self.purchase_order.po_number, "PO123")
        self.assertEqual(self.purchase_order.vendor, self.vendor)
        self.assertAlmostEqual(self.purchase_order.order_date, timezone.now())
        self.assertAlmostEqual(self.purchase_order.delivery_date, timezone.now() + timedelta(days=7))
        self.assertEqual(self.purchase_order.items, [{"item_code": "ITEM-1", "description": "Product X", "quantity": 5}])
        self.assertEqual(self.purchase_order.quantity, 5)
        self.assertEqual(self.purchase_order.status, "pending")
        self.assertEqual(self.purchase_order.quality_rating, None)
        self.assertAlmostEqual(self.purchase_order.issue_date, timezone.now())
        self.assertEqual(self.purchase_order.acknowledgment_date, None)

    def test_purchase_order_default_values(self):
        # Test default values
        new_order = PurchaseOrder.objects.create(
            po_number='PO124',
            vendor=self.vendor,
            delivery_date=timezone.now() + timezone.timedelta(days=14),
            items=[{'item_name': 'Item2', 'quantity': 3, 'price': 15.0}],
            quantity=3,
            status='pending',
            issue_date=timezone.now(),
        )
        self.assertIsNone(new_order.quality_rating)
        self.assertIsNone(new_order.acknowledgment_date)
    
    def test_purchase_order_choices(self):
        # Test valid status choices
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        for status in valid_statuses:
            self.purchase_order.status = status
            self.purchase_order.save()
            self.assertEqual(self.purchase_order.status, status)

    def test_purchase_order_status_transition(self):
        self.assertEqual(self.purchase_order.status, 'pending')
        self.purchase_order.status = 'completed'
        self.purchase_order.save()
        self.assertEqual(self.purchase_order.status, 'completed')

    def test_purchase_order_with_quality_rating(self):
        new_order = PurchaseOrder.objects.create(
            po_number='PO126',
            vendor=self.vendor,
            delivery_date=timezone.now() + timezone.timedelta(days=14),
            items=[{'item_name': 'Item5', 'quantity': 1, 'price': 20.0}],
            quantity=1,
            status='completed',
            quality_rating=4.5,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
        )
        self.assertEqual(new_order.quality_rating, 4.5)
