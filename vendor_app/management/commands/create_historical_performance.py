import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from vendor_app.models import Vendor, HistoricalPerformance

fake = Faker()

class Command(BaseCommand):
    help = 'Create sample Historical Performance data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample Historical Performance data...'))

        vendors = Vendor.objects.all()

        for vendor in vendors:
            for _ in range(random.randint(5, 15)):
                historical_performance = HistoricalPerformance.objects.create(
                    vendor=vendor,
                    date=fake.date_time_this_year(),
                    on_time_delivery_rate=random.uniform(80, 100),
                    quality_rating_avg=random.uniform(3, 5),
                    average_response_time=random.uniform(1, 10),
                    fulfillment_rate=random.uniform(90, 100),
                )

        self.stdout.write(self.style.SUCCESS('Sample Historical Performance data created successfully!'))
