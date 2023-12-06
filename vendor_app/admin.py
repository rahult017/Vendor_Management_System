from django.contrib import admin
from vendor_app.models import Vendor,PurchaseOrder,HistoricalPerformance
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Vendor,PurchaseOrder,HistoricalPerformance

class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor

class VendorAdmin(ImportExportModelAdmin):
    resource_class = VendorResource
    list_display = ('name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    search_fields = ('name', 'vendor_code', 'contact_details')

class PurchaseOrderResource(resources.ModelResource):
    class Meta:
        model = PurchaseOrder

class PurchaseOrderAdmin(ImportExportModelAdmin):
    resource_class = PurchaseOrderResource
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'status')
    search_fields = ('po_number', 'vendor__name', 'status')
    list_filter = ('status', 'delivery_date')
    date_hierarchy = 'delivery_date'
    ordering = ('delivery_date',)

class HistoricalPerformanceResource(resources.ModelResource):
    class Meta:
        model = HistoricalPerformance

class HistoricalPerformanceAdmin(ImportExportModelAdmin):
    resource_class = HistoricalPerformanceResource
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    list_filter = ('vendor__name', 'date')
    search_fields = ('vendor__name',)
    date_hierarchy = 'date'
    ordering = ('date',)

admin.site.register(Vendor,VendorAdmin)
admin.site.register(PurchaseOrder,PurchaseOrderAdmin)
admin.site.register(HistoricalPerformance,HistoricalPerformanceAdmin)
