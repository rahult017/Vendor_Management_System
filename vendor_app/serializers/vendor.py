from rest_framework import serializers
from vendor_app.models import Vendor
import logging

logger = logging.getLogger(__name__)

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'