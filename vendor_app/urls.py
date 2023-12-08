from django.urls import path
from vendor_app.views.vendor import (VendorListCreateView,VendorDetailView,VendorPerformanceView)
from vendor_app.views.purchaseorder import (PurchaseOrderListCreateView,
                    PurchaseOrderDetailView,AcknowledgePurchaseView)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/',obtain_auth_token,name='obtain-token'),
    path('vendors/',VendorListCreateView.as_view(),name="vendor_list_create"),
    path('vendors/<int:vendor_id>/',VendorDetailView.as_view(),name='vendor_detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase_order_list_create'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseView.as_view(), name='acknowledge_purchase'),
]