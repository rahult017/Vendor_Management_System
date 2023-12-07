from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from vendor_app.models import Vendor, PurchaseOrder
from vendor_app.serializers.vendor import VendorSerializer
from vendor_app.serializers.purchase import PurchaseOrderSerializer


class VendorAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': '123-456-7890',
            'address': 'Test Address',
            'vendor_code': 'testcode',
            'on_time_delivery_rate': 0.0,
            'quality_rating_avg': 0.0,
            'average_response_time': 0.0,
            'fulfillment_rate': 0.0
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('vendor_list_create')
    
    def test_vendor_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_vendor(self):
        new_vendor_data = {
            'name': 'New Vendor',
            'contact_details': '987-654-3210',
            'address': 'New Address',
            'vendor_code': 'newcode',
            'on_time_delivery_rate': 0.0,
            'quality_rating_avg': 0.0,
            'average_response_time': 0.0,
            'fulfillment_rate': 0.0
        }

        response = self.client.post(self.url, new_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_vendor_detail(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')

    def test_update_vendor(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        updated_data = {
            'name': 'Updated Vendor',
            'contact_details': '999-999-9999',
            'address': 'Updated Address',
            'vendor_code': 'updatedcode',
            'on_time_delivery_rate': 1.0,
            'quality_rating_avg': 1.0,
            'average_response_time': 1.0,
            'fulfillment_rate': 1.0
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Vendor')
    
    def test_delete_vendor(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)
