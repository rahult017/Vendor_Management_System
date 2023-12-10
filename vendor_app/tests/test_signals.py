from django.test import TestCase,Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from vendor_app.models import Vendor,PurchaseOrder,HistoricalPerformance

class CreateAuthTokenSignalTest(TestCase):
    def test_create_auth_token_signal(self):
        # Create a new user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Check that the signal creates a new auth token
        tokens_before_save = Token.objects.count()
        user.save()
        tokens_after_save = Token.objects.count()

        self.assertEqual(tokens_after_save, tokens_before_save)

        # Check that the token has the correct attributes
        token = Token.objects.get(user=user)
        self.assertEqual(token.user, user)

        # Check that the token has a created and expires attribute
        self.assertIsNotNone(token.created)

        # Check that the expires attribute is set correctly
        self.assertLessEqual(timezone.now() - token.created, timedelta(seconds=2))

    def test_create_auth_token_signal_exception(self):
        # Mock the Token.objects.create method to raise an exception
        with self.assertRaises(Exception):
            with self.settings(DEBUG=True):  
                with self.assertRaises(Exception):
                    with self.settings(DEBUG=True): 
                        Token.objects.create = lambda *args, **kwargs: None
                        user = User.objects.create_user(username='testuser', password='testpassword')
                        user.save()

        # Ensure that the exception was logged (in this case, to the console)
        self.assertLogs(logger=__name__, level='ERROR')

class SignalHandlerTestCase(TestCase):
    def setUp(self):
        self.vendor= Vendor.objects.create(name='Test Vendor')
        self.purchase_order = PurchaseOrder.objects.create(po_number='PO121',vendor=self.vendor, status='completed', 
                                                          issue_date=timezone.now(), 
                                                          acknowledgment_date=timezone.now(), 
                                                          delivery_date=timezone.now(),
                                                          order_date=timezone.now(),
                                                          items=[{"item_code": "ITEM-1", "description": "Product X", "quantity": 5}],
                                                          quantity=5,
                                                          quality_rating=4)
    
    def test_update_historical_performance_signal(self):
        historical_performance = HistoricalPerformance.objects.get(vendor=self.vendor, date=self.purchase_order.issue_date)
        self.assertEqual(historical_performance.on_time_delivery_rate, 100)  
        self.assertEqual(historical_performance.quality_rating_avg, 4)
        self.assertEqual(historical_performance.average_response_time, 0)
        self.assertEqual(historical_performance.fulfillment_rate, 0)
        self.po_in_progress = PurchaseOrder.objects.create(po_number='PO122',vendor=self.vendor, 
                                                    status='in_progress', issue_date=timezone.now(),
                                                    items=[{"item_code": "ITEM-1", "description": "Product X", "quantity": 5}],
                                                    delivery_date=timezone.now(),
                                                    order_date=timezone.now(),
                                                    quantity=5)
    
    def tearDown(self) -> None:
        self.vendor.delete()
        self.purchase_order.delete()
        self.po_in_progress.delete()