from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar_ecom.settings import ROZARPAY_API_KEY, ROZARPAY_API_SECRET
import razorpay

class PaymentDetailsView(CorePaymentDetailsView):
    
    def handle_place_order_submission(self, request):
        razorpay_order_id = request.session.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')

        # Verify the payment signature
        client = razorpay.Client(auth=(ROZARPAY_API_KEY,ROZARPAY_API_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            # If payment is verified, proceed to place the order
            return self.submit(**self.build_submission())
        except razorpay.errors.SignatureVerificationError:
            # Handle verification error (payment failed)
            return self.render_payment_details(request, error="Payment verification failed")


    def handle_payment_details_submission(self, request):

        # Initialize Razorpay client
        client = razorpay.Client(auth=(ROZARPAY_API_KEY,ROZARPAY_API_SECRET))
        
        # Extract form data (e.g., order amount, currency)
        basket = self.request.basket
        total_incl_tax = basket.total_incl_tax
        amount = int(total_incl_tax * 100)  # Convert to paise for Razorpay (e.g., 500.00 INR -> 50000 paise)
        currency = "INR"

        
        # Create an order on Razorpay
        razorpay_order = client.order.create(dict(amount = amount, currency = currency, payment_capture = 1))

        # Save order_id in session or database for verification later
        request.session['razorpay_order_id'] = razorpay_order['id']

        context = {
            'amount': 20000,
            'api_key': "rzp_test_6bIJl2FhugXCH6",  # Make sure this is correctly defined
            'order_id': razorpay_order['id']
        }
        # Render the preview page with Razorpay order details
        return render(request,'oscar/checkout/payment_detail.html',context)
    