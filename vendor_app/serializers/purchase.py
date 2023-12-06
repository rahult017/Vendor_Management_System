from rest_framework import serializers
from vendor_app.models import PurchaseOrder
import logging

logger = logging.getLogger(__name__)

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'