from django.test import TestCase
from datetime import datetime
from .models import PurchaseOrder, HistoricalPerformance,Vendor
from vendor_app.signals import update_historical_performance
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

fake = Faker()

class SignalHandlerTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.all()
        # Create a PurchaseOrder instance
        self.purchase_order= PurchaseOrder.objects.create(
                    po_number=fake.uuid4(),
                    vendor=self.vendor,
                    order_date=fake.date_time_this_year(),
                    delivery_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                    items={'item': fake.word()},
                    quantity=random.randint(1, 100),
                    status=random.choice(['pending', 'in_progress', 'completed', 'cancelled']),
                    quality_rating=random.choice([None, random.uniform(1, 5)]),
                    issue_date=fake.date_time_this_year(),
                    acknowledgment_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                )
    def test_signal_handler_called(self):
        print(self.vendor)
        # Check if the signal handler was called when the PurchaseOrder was created
        self.assertTrue(update_historical_performance.called)

    def test_historical_performance_record_updated(self):
        # Check if the historical performance record was updated with the expected values
        historical_performance = HistoricalPerformance.objects.get(vendor=self.purchase_order.vendor, date=datetime.date.today())
        self.assertEqual(historical_performance.on_time_delivery_rate, 1.0)
        self.assertEqual(historical_performance.quality_rating_avg, 5.0)
        self.assertEqual(historical_performance.average_response_time, 0.0)
        self.assertEqual(historical_performance.fulfillment_rate, 1.0)
