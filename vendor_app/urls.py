from django.urls import path
from .views import vendor_performance,vendor_list_create

urlpatterns = [
    path('vendors/',vendor_list_create,name="vendor_list_create"),
    path('vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor_performance'),
]