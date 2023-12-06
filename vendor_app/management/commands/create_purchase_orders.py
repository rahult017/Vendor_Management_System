import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from vendor_app.models import Vendor, PurchaseOrder

fake = Faker()

class Command(BaseCommand):
    help = 'Create sample Purchase Orders data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample Purchase Orders data...'))

        vendors = Vendor.objects.all()

        for vendor in vendors:
            # Shuffle the list of status values to introduce more randomness
            for _ in range(1, 11):
                status_options = ['pending', 'in_progress', 'completed', 'cancelled']
                random.shuffle(status_options)
                # Check if the list is empty, shuffle again
                po = PurchaseOrder.objects.create(
                    po_number=fake.uuid4(),
                    vendor=vendor,
                    order_date=fake.date_time_this_year(),
                    delivery_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                    items={'item': fake.word()},
                    quantity=random.randint(1, 100),
                    status=status_options.pop(),
                    quality_rating=random.choice([None, random.uniform(1, 5)]),
                    issue_date=fake.date_time_this_year(),
                    acknowledgment_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                )

        self.stdout.write(self.style.SUCCESS('Sample Purchase Orders data created successfully!'))
