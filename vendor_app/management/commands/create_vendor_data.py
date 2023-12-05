# vendor_app/management/commands/create_sample_data.py
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from vendor_app.models import Vendor, PurchaseOrder

fake = Faker()

class Command(BaseCommand):
    help = 'Create sample data with 10 vendors'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        for _ in range(10):
            vendor = Vendor.objects.create(
                name=fake.company(),
                contact_details=fake.phone_number(),
                address=fake.address(),
                vendor_code=fake.uuid4(),
            )

            for _ in range(random.randint(5, 15)):
                po = PurchaseOrder.objects.create(
                    po_number=fake.uuid4(),
                    vendor=vendor,
                    order_date=fake.date_time_this_year(),
                    delivery_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                    items={'item': fake.word()},
                    quantity=random.randint(1, 100),
                    status=random.choice(['pending', 'completed', 'canceled']),
                    quality_rating=random.choice([None, random.uniform(1, 5)]),
                    issue_date=fake.date_time_this_year(),
                    acknowledgment_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
