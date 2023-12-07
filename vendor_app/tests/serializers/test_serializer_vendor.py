from django.test import TestCase
from rest_framework.test import APITestCase
from vendor_app.models import Vendor
from vendor_app.serializers.vendor import VendorSerializer
from rest_framework import status


class VendorSerializerTestCase(TestCase):
    def setUp(self):
        self.vendor_data = {
            "name":"Test Vendor",
            "contact_details":"Test Contact Details",
            "address":"Test Address",
            "vendor_code":"TEST123"
        }
    
    def test_vendor_serializer_valid_data(self):
        serializer = VendorSerializer(data=self.vendor_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        
    
    def test_vendor_serializer_invalid_data(self):
        invalid_data = {
            "name":"",
            "contact_details":"Test Contact Details",
            "address":"Test Address",
            "vendor_code":"TEST123"
        }
        serializer = VendorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
    
    def test_vendor_serializer_update(self):
        vendor = Vendor.objects.create(name="Test Vendor",contact_details="Test Contact Details",
                                       address="Test Address",
                                       vendor_code="TEST123")
        serializer = VendorSerializer(instance=vendor, data=self.vendor_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        vendor.refresh_from_db()
        self.assertEqual(vendor.name, self.vendor_data['name'])
        self.assertEqual(vendor.contact_details, self.vendor_data['contact_details'])
        self.assertEqual(vendor.address, self.vendor_data['address'])
        self.assertEqual(vendor.vendor_code, self.vendor_data['vendor_code'])
    
    def test_vendor_serializer_delete(self):
        vendor = Vendor.objects.create(name="Test Vendor",contact_details="Test Contact Details",
                                       address="Test Address",
                                       vendor_code="TEST123")
        
        serializer = VendorSerializer(instance=vendor)
        vendor.delete()
        initial_count = Vendor.objects.count()
        self.assertEqual(Vendor.objects.count(), initial_count)
        deleted_vendor = Vendor.objects.filter(name='Test Vendor').first()
        self.assertIsNone(deleted_vendor)
        