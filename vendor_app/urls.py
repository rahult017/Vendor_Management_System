from django.urls import path
from .views import vendor_performance

urlpatterns = [
    path('vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor_performance'),
]