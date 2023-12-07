from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from vendor_app.models import Vendor, PurchaseOrder
from vendor_app.serializers.purchase import PurchaseOrderSerializer


class PurchaseOrderAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
            vendor_code="TEST123"
        )
        # Create a test purchase order
        self.po_data = {
            'po_number': 'PO123',
            'vendor': self.vendor,
            'order_date': '2023-01-01T00:00:00Z',
            'delivery_date': '2023-01-10T00:00:00Z',
            'items': [],
            'quantity': 10,
            'status': 'pending',
            'issue_date': '2023-01-02T00:00:00Z',
            'acknowledgment_date': '2023-01-03T00:00:00Z'
        }
        self.po = PurchaseOrder.objects.create(**self.po_data)

        # Set up authentication for the test client
        self.client.force_authenticate(user=self.user)
    
    def test_purchaseorder_list(self):
        url = reverse('purchase_order_list_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_purchaseorder(self):
        url = reverse('purchase_order_list_create')
        new_po_data = {
            'po_number': 'PO456',
            'vendor': self.vendor.id,
            'order_date': '2023-02-01T00:00:00Z',
            'delivery_date': '2023-02-10T00:00:00Z',
            'items': [],
            'quantity': 20,
            'status': 'in_progress',
            'issue_date': '2023-02-02T00:00:00Z',
            'acknowledgment_date': '2023-02-03T00:00:00Z'
        }

        response = self.client.post(url, new_po_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)
    
    def test_update_purchaseorder(self):
        url = reverse('purchase_order_detail', args=[self.po.id])
        updated_data = {
            'po_number': 'PO456',
            'vendor': self.vendor.id,
            'order_date': '2023-02-01T00:00:00Z',
            'delivery_date': '2023-02-10T00:00:00Z',
            'items': [],
            'quantity': 25,
            'status': 'completed',
            'issue_date': '2023-02-02T00:00:00Z',
            'acknowledgment_date': '2023-02-03T00:00:00Z'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 25)

    def test_delete_purchaseorder(self):
        url = reverse('purchase_order_detail', args=[self.po.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)
