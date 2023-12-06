from django.test import TestCase
from vendor_app.models import Vendor
from django.db.utils import IntegrityError
import logging

logger = logging.getLogger(__name__)


class VendorModelTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
            vendor_code="TEST123"
        )
    
    def test_vendor_str_method(self):
        expected_str = "Test Vendor"
        self.assertEqual(str(self.vendor), expected_str)
    
    def test_default_values(self):
        # Test that the default values are set correctly
        self.assertEqual(self.vendor.on_time_delivery_rate, 0)
        self.assertEqual(self.vendor.quality_rating_avg, 0)
        self.assertEqual(self.vendor.average_response_time, 0)
        self.assertEqual(self.vendor.fulfillment_rate, 0)
    
    def test_vendor_creation(self):
        # Test the creation of a Vendor instance
        vendor_count_before = Vendor.objects.count()

        new_vendor = Vendor.objects.create(
            name="New Vendor",
            contact_details="New Contact Details",
            address="New Address",
            vendor_code="NEW123"
        )

        vendor_count_after = Vendor.objects.count()

        # Check that the vendor count has increased by 1
        self.assertEqual(vendor_count_after, vendor_count_before + 1)

        # Check the attributes of the new vendor
        self.assertEqual(new_vendor.name, "New Vendor")
        self.assertEqual(new_vendor.contact_details, "New Contact Details")
        self.assertEqual(new_vendor.address, "New Address")
        self.assertEqual(new_vendor.vendor_code, "NEW123")

    def test_vendor_creation_all_fields(self):
        # Test creating a Vendor instance with all fields
        vendor = Vendor.objects.create(
            name="Full Vendor",
            contact_details="Full Contact Details",
            address="Full Address",
            vendor_code="FULL123",
            on_time_delivery_rate=0.8,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=0.9
        )
        self.assertEqual(vendor.name, "Full Vendor")
        self.assertEqual(vendor.on_time_delivery_rate, 0.8)
        self.assertEqual(vendor.quality_rating_avg, 4.5)
        self.assertEqual(vendor.average_response_time, 2.5)
        self.assertEqual(vendor.fulfillment_rate, 0.9)

    def test_vendor_unique_vendor_code(self):
        # Test that the vendor_code is unique
        with self.assertRaises(IntegrityError):
            Vendor.objects.create(
                name="Test Vendor",
                contact_details="Duplicate Contact Details",
                address="Duplicate Address",
                vendor_code=None
            )