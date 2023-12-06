from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .models import PurchaseOrder,HistoricalPerformance
from django.db import transaction
from vendor_app.utils import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
    calculate_average_response_time,
    calculate_fulfillment_rate,
)
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            Token.objects.create(user=instance).delete()
            
            # Create a new token with expiration (customize timedelta as needed)
            expiration_time = timedelta(days=1)  # Adjust as needed
            expiration_date = instance.date_joined + expiration_time

            token = Token.objects.create(user=instance)
            token.created = instance.date_joined
            token.expires = expiration_date
            token.save()
        except Exception as e:
            # Handle the exception (e.g., log it)
            print(f"Error creating token for new user {instance}: {e}")


receiver(post_save, sender=PurchaseOrder)
def update_historical_performance(sender,instance,**kwargs):
    """
    Signal handler to update historical performance records when a new PurchaseOrder is created.
    """

    vendor = instance.vendor

    @transaction.atomic
    def update_performance_metrics_batch(vendor):

        # Calculate on-time delivery rate and quality rating average
        on_time_deliveries = calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = calculate_quality_rating_avg(vendor)

        # Calculate additional metrics
        average_response_time = calculate_average_response_time(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)

        # Update HistoricalPerformance model
        historical_performance, created = HistoricalPerformance.objects.get_or_create(
            vendor=vendor,
            date=instance.issue_date,
            defaults={
                'on_time_delivery_rate': on_time_deliveries,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time': average_response_time,
                'fulfillment_rate': fulfillment_rate,
            }
        )
        if not created:
            historical_performance.on_time_delivery_rate = on_time_deliveries
            historical_performance.quality_rating_avg = quality_rating_avg
            historical_performance.average_response_time = average_response_time
            historical_performance.fulfillment_rate = fulfillment_rate
            historical_performance.save()

    if instance.status == 'completed' or instance.status == 'acknowledged':
        update_performance_metrics_batch(vendor)

post_save.connect(create_auth_token,sender=User)
post_save.connect(update_historical_performance, sender=PurchaseOrder)