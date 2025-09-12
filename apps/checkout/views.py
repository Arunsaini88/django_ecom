from oscar.apps.checkout import views
from oscar.apps.payment import models
from oscar.apps.payment.exceptions import PaymentError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from oscar.apps.payment.models import Source, SourceType
from django.conf import settings


import razorpay  # Razorpay SDK for API interaction
from razorpay.errors import BadRequestError, ServerError

from django.http import JsonResponse, HttpResponse


class PaymentDetailsView(views.PaymentDetailsView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Pass Razorpay-specific data to the template for rendering the payment form.
        """
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))

        # Generate Razorpay order
        order_number = self.generate_order_number(self.request.basket)
        total_incl_tax = self.request.basket.total_incl_tax
        razorpay_order = client.order.create({
            "amount": int(ctx['order_total'].incl_tax * 100),  # Amount in paise
            "currency": "INR",
            "receipt": str(order_number),
            "payment_capture": 1
        })

        # Add Razorpay details to the context
        ctx['razorpay_key'] = settings.RAZORPAY_PUBLISHABLE_KEY
        ctx['razorpay_order_id'] = razorpay_order['id']
        ctx['basket_total'] = ctx['order_total'].incl_tax * 100
        ctx['order_number'] = order_number
        ctx['user_email'] = self.request.user.email if self.request.user.is_authenticated else ''
        # print(ctx)
        return ctx

    def handle_payment(self, order_number, total, **kwargs):
        """
        Validate the Razorpay payment after it's completed on the frontend.
        """
        razorpay_payment_id = kwargs.get('razorpay_payment_id')

        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))

        try:
            # Verify the payment
            payment = client.payment.fetch(razorpay_payment_id)
            if payment['status'] != 'captured':
                raise PaymentError("Payment not captured")

            # Record payment source
            source_type, __ = models.SourceType.objects.get_or_create(name="Razorpay")
            source = models.Source(
                source_type=source_type,
                amount_allocated=total.incl_tax,
                reference=razorpay_payment_id
            )
            self.add_payment_source(source)

            # Record payment event
            self.add_payment_event('captured', total.incl_tax)

        except PaymentError as e:
            raise PaymentError(f"Payment validation failed: {e}")
        except Exception as e:
            raise PaymentError(f"Unexpected error during payment handling: {e}")
