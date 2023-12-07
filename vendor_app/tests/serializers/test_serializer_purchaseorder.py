from django.test import TestCase
from rest_framework.test import APITestCase
from vendor_app.models import Vendor,PurchaseOrder
from vendor_app.serializers.purchase import PurchaseOrderSerializer
from rest_framework import status


class PurchaseOrderSerializerTestCase(TestCase):

    def setUp(self):

        self.vendor = Vendor.objects.create(name='Test Vendor',
                                            contact_details="Test Contact Details",
                                            address="Test Address",
                                            vendor_code="TEST123")

        # Create a PurchaseOrder instance for testing
        self.purchase_order_data = {
            'po_number': 'PO123',
            'vendor': self.vendor.id,
            'order_date': '2023-01-01T12:00:00Z',
            'delivery_date': '2023-01-15T12:00:00Z',
            'items': [{'item_name': 'Item1', 'quantity': 5, 'price': 10.0}],
            'quantity': 5,
            'status': 'pending',
            'quality_rating': 4.5,
            'issue_date': '2023-01-05T12:00:00Z',
            'acknowledgment_date': '2023-01-10T12:00:00Z',
        }

    def test_purchase_order_serializer_valid_data(self):
        serializer = PurchaseOrderSerializer(data=self.purchase_order_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
    
    def test_purchase_order_serializer_invalid_data(self):
        invalid_data = {
            'po_number': 'PO124',
            'order_date': '2023-01-01T12:00:00Z',
            'delivery_date': '2023-01-15T12:00:00Z',
            'quantity': 5,
            'status': 'pending',
            'quality_rating': 4.5,
            'issue_date': '2023-01-05T12:00:00Z',
            'acknowledgment_date': '2023-01-10T12:00:00Z',
        }
        serializer = PurchaseOrderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_purchase_order_serializer_update(self):
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date='2023-01-01T12:00:00Z',
            delivery_date='2023-01-15T12:00:00Z',
            items=[{'item_name': 'Item1', 'quantity': 5, 'price': 10.0}],
            quantity=5,
            status='pending',
            quality_rating=4.5,
            issue_date='2023-01-05T12:00:00Z',
            acknowledgment_date='2023-01-10T12:00:00Z',
        )

        updated_data = {
            'po_number': 'PO123',
            'vendor': self.vendor.id,
            'order_date': '2023-01-01T12:00:00Z',
            'delivery_date': '2023-01-20T12:00:00Z',
            'items': [{'item_name': 'Item1', 'quantity': 5, 'price': 12.0}],  
            'quantity': 7,  
            'status': 'completed',  
            'quality_rating': 4.8,  
            'issue_date': '2023-01-05T12:00:00Z',
            'acknowledgment_date': '2023-01-10T12:00:00Z',
        }
        serializer = PurchaseOrderSerializer(instance=purchase_order, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        purchase_order.refresh_from_db()
        self.assertEqual(purchase_order.po_number, updated_data['po_number'])
       

    def test_purchase_order_serializer_delete(self):
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date='2023-01-01T12:00:00Z',
            delivery_date='2023-01-15T12:00:00Z',
            items=[{'item_name': 'Item1', 'quantity': 5, 'price': 10.0}],
            quantity=5,
            status='pending',
            quality_rating=4.5,
            issue_date='2023-01-05T12:00:00Z',
            acknowledgment_date='2023-01-10T12:00:00Z',
        )
        serialized_data = PurchaseOrderSerializer(instance=purchase_order)
        purchase_order.delete()
        initial_count = PurchaseOrder.objects.count()
        self.assertEqual(PurchaseOrder.objects.count(), initial_count)
        deleted_purchase_order = PurchaseOrder.objects.filter(po_number='PO123').first()
        self.assertIsNone(deleted_purchase_order)
        