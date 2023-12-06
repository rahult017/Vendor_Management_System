from rest_framework import serializers
from vendor_app.models import HistoricalPerformance
import logging

logger = logging.getLogger(__name__)

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'