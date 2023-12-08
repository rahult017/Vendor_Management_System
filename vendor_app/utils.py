from django.db import models
from django.db.models import Avg
import logging

logger = logging.getLogger(__name__)

def calculate_on_time_delivery_rate(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=models.F('acknowledgment_date'))
    on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100  if completed_pos.count() > 0 else 0
    return on_time_delivery_rate

def calculate_quality_rating_avg(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
    quality_rating_avg = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    return quality_rating_avg

def calculate_average_response_time(vendor):
    acknowledged_pos = vendor.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
    response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]
    average_response_time = sum(response_times) / len(acknowledged_pos) if len(acknowledged_pos) > 0 else 0
    return average_response_time

def calculate_fulfillment_rate(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    successful_fulfillments = completed_pos.filter(issue_date__lte=models.F('acknowledgment_date'), quality_rating__isnull=True)
    fulfillment_rate = (successful_fulfillments.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0
    return fulfillment_rate
