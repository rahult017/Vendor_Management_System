from django.test import TestCase
from django.utils import timezone
from vendor_app.models import Vendor,PurchaseOrder
from vendor_app.utils import(calculate_on_time_delivery_rate,calculate_quality_rating_avg,
                             calculate_average_response_time,calculate_fulfillment_rate)

class VendorMetricsTestCase(TestCase):
    def setUp(self):
        # Create a vendor and purchase orders for testing
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.completed_po1 = PurchaseOrder.objects.create(po_number='PO121',vendor=self.vendor, status='completed', 
                                                          issue_date=timezone.now(), 
                                                          acknowledgment_date=timezone.now(), 
                                                          delivery_date=timezone.now(),
                                                          order_date=timezone.now(),
                                                          items=[{"item_code": "ITEM-1", "description": "Product X", "quantity": 5}],
                                                          quantity=5)
        self.completed_po2 = PurchaseOrder.objects.create(po_number='PO122',vendor=self.vendor, status='completed', 
                                                          issue_date=timezone.now(), 
                                                          acknowledgment_date=timezone.now(), 
                                                          delivery_date=timezone.now(),
                                                          order_date=timezone.now(),
                                                          items=[{"item_code": "ITEM-2", "description": "Product Y", "quantity": 15}],
                                                          quantity=15)
        self.incomplete_po = PurchaseOrder.objects.create(po_number='PO123',vendor=self.vendor, status='pending', 
                                                          issue_date=timezone.now(),
                                                          order_date=timezone.now(),
                                                          delivery_date=timezone.now(),
                                                          items=[{"item_code": "ITEM-2", "description": "Product Y", "quantity": 15}],
                                                          quantity=15)
    def tearDown(self):
        # Clean up objects created during setup
        self.vendor.delete()
        self.completed_po1.delete()
        self.completed_po2.delete()
        self.incomplete_po.delete()
    
    def test_calculate_on_time_delivery_rate(self):
        self.assertEqual(calculate_on_time_delivery_rate(self.vendor), 100)

    def test_calculate_quality_rating_avg(self):
        # Set quality ratings for completed purchase orders
        self.completed_po1.quality_rating = 4
        self.completed_po1.save()
        self.completed_po2.quality_rating = 5
        self.completed_po2.save()

        self.assertEqual(calculate_quality_rating_avg(self.vendor), 4.5)
    
    def test_calculate_average_response_time(self):
        # Set acknowledgment dates for completed purchase orders
        self.completed_po1.acknowledgment_date = timezone.now() + timezone.timedelta(hours=1)
        self.completed_po1.save()
        self.completed_po2.acknowledgment_date = timezone.now() + timezone.timedelta(hours=2)
        self.completed_po2.save()

        expected_average_response_time = ((self.completed_po1.acknowledgment_date - self.completed_po1.issue_date).total_seconds() +
                                          (self.completed_po2.acknowledgment_date - self.completed_po2.issue_date).total_seconds()) / 2

        self.assertEqual(calculate_average_response_time(self.vendor), expected_average_response_time)

    def test_calculate_fulfillment_rate(self):
        fulfillment_rate = calculate_fulfillment_rate(self.vendor)
        self.assertEqual(fulfillment_rate, 100.0) 