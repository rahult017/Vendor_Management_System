# Vendor Management System with Performance Metrics

To check how to use below api please refer to api_videos in the project.

1.Vendor Profile Management

    POST  /api/token/: Generate auth token.
    POST /api/vendors/: Create a new vendor.
    GET /api/vendors/: List all vendors.
    GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
    PUT /api/vendors/{vendor_id}/: Update a vendor's details
    DELETE /api/vendors/{vendor_id}/: Delete a vendor.
    

2.Purchase Order Tracking

    POST /api/purchase_orders/: Create a purchase order.
    GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
    GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
    PUT /api/purchase_orders/{po_id}/: Update a purchase order.
    DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
    

3. Vendor Performance

    GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance.
    POST /api/purchase_orders/{po_id}/acknowledge/ : create vendors to acknowledge POs.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rahult017/Vendor_Management_System.git
   cd Vendor_Management_System

2. Set up the virtual environment and install dependencies:

    To create virtual environment: python -m venv venv

    # For Unix/Linux
    source venv/bin/activate

    # For Windows
    .\venv\Scripts\activate

    pip install -r requirements.txt

3. Apply migrations and create a superuser account:

```bash
   python manage.py makemigrations vendor_app
   python manage.py migrate
   python manage.py createsuperuser


4. Run the development server

    python manage.py runserver
   
3. Create Sample Data for project:

    python manage.py create_vendor_data        ## to create a sample data for vendor profile management
    python  manage.py create_purchase_orders   ## to create a sample data for purchase order

$. Run test case :
    
    python manage.py test vendor_app.tests.models.test_vendor_models
    python manage.py test vendor_app.tests.models.test_purchase_models
    python manage.py test vendor_app.tests.serializers.test_serializer_vendor
    python manage.py test vendor_app.tests.serializers.test_serializer_purchaseorder
    python manage.py test vendor_app.tests.views.test_views_vendor
    python manage.py test vendor_app.tests.views.test_views_purchaseorder
    python manage.py test vendor_app.tests.test_utils
    python manage.py test vendor_app.tests.test_signals

