from django.db import models
from vendor_app.utils import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
    calculate_average_response_time,
    calculate_fulfillment_rate,
)

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def update_performance_metrics(self):
        # Calculate and update performance metrics
        self.on_time_delivery_rate = calculate_on_time_delivery_rate(self)
        self.quality_rating_avg = calculate_quality_rating_avg(self)
        self.average_response_time = calculate_average_response_time(self)
        self.fulfillment_rate = calculate_fulfillment_rate(self)
        self.save()

    def __str__(self) -> str:
        return self.name
