from django.urls import path
from vendor_app.views.vendor import (vendor_list_create,vendor_detail,vendor_performance)
from vendor_app.views.purchaseorder import (purchase_order_list_create,
                    purchase_order_detail,acknowledge_purchase)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/',obtain_auth_token,name='obtain-token'),
    path('vendors/',vendor_list_create,name="vendor_list_create"),
    path('vendors/<int:vendor_id>/',vendor_detail,name='vendor_detail'),
    path('vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor_performance'),
    path('purchase_orders/',purchase_order_list_create,name='purchase_order_list_create'),
    path('purchase_orders/<int:po_id>/',purchase_order_detail,name='purchase_order_detail'),
    path('purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase, name='acknowledge_purchase'),
]