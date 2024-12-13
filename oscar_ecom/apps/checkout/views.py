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


    # def handle_place_order_submission(self, request):
    #     """
    #     Validate the Razorpay payment on the backend before placing the order.
    #     """
    #     razorpay_payment_id = request.POST.get('razorpay_payment_id')

    #     # Initialize Razorpay client
    #     client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))

    #     try:
    #         # Verify payment details
    #         payment = client.payment.fetch(razorpay_payment_id)
    #         if payment['status'] != 'captured':
    #             raise PaymentError("Payment not captured")

    #         # Proceed with order placement
    #         return super().handle_place_order_submission(request)

    #     except BadRequestError as e:
    #         print(f"BadRequestError: {e}")
    #         return JsonResponse({"error": "Invalid payment request"}, status=400)
    #     except ServerError as e:
    #         print(f"ServerError: {e}")
    #         return JsonResponse({"error": "Payment server error. Please try again later."}, status=500)
    #     except Exception as e:
    #         print(f"Unexpected Error: {e}")
    #         return JsonResponse({"error": "Unexpected error occurred"}, status=500)




















# views.py
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views.decorators.csrf import csrf_exempt
# from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
# from oscar.apps.payment.models import Source, SourceType
# from django.conf import settings
# import razorpay
# from . import forms

# class PaymentDetailsView(CorePaymentDetailsView):

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
#         client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))
#         if self.preview:
#             ctx['razorpay_token_form'] = forms.RazorpayPaymentForm(self.request.POST)
#             ctx['order_total_incl_tax_cents'] = (
#                 ctx['order_total'].incl_tax * 100
#             ).to_integral_value()
#         else:
#             ctx['order_total_incl_tax_cents'] = (
#                     ctx['order_total'].incl_tax * 100
#             ).to_integral_value()
#             ctx['razorpay_publishable_key'] = settings.RAZORPAY_PUBLISHABLE_KEY
#             data = {
#                 'amount': int(ctx['order_total'].incl_tax * 100),
#                 'currency': 'INR',
#                 'receipt': str(self.request.basket.id)
#             }
#             order = client.order.create(data=data)
#             ctx['razorpay_order_id'] = order['id']
#         return ctx

#     def handle_payment(self, order_number, total, **kwargs):
#         client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))
#         order_amount = int(total.incl_tax * 100)  # amount in paise
#         order_currency = 'INR'
#         order_receipt = order_number

#         order = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt))
#         razorpay_order_id = order['id']

#         # Save the order ID in the session to verify the payment later
#         self.request.session['razorpay_order_id'] = razorpay_order_id

#         razorpay_ref = client.payment.capture(
#             self.request.POST['razorpay_payment_id'],
#             order_amount
#         )

#         source_type, __ = SourceType.objects.get_or_create(name="Razorpay")
#         source = Source(
#             source_type=source_type,
#             currency='INR',
#             amount_allocated=total.incl_tax,
#             amount_debited=total.incl_tax,
#             reference=razorpay_ref['id']
#         )
#         self.add_payment_source(source)

#         self.add_payment_event('purchase', total.incl_tax)

#     def post(self, request, *args, **kwargs):
#         form = forms.RazorpayTokenForm(request.POST)
#         if form.is_valid():
#             client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))
#             params_dict = {
#                 'razorpay_order_id': form.cleaned_data['razorpay_order_id'],
#                 'razorpay_payment_id': form.cleaned_data['razorpay_payment_id'],
#                 'razorpay_signature': form.cleaned_data['razorpay_signature']
#             }

#             try:
#                 client.utility.verify_payment_signature(params_dict)
#                 self.handle_payment(request.basket.order_number, request.basket.total_incl_tax)
#                 return redirect(reverse('checkout:thank-you'))
#             except:
#                 return self.render_preview(request, error="Payment verification failed")
#         return self.render_preview(request, error="Invalid form submission")

# import razorpay
# from django.conf import settings
# from django.shortcuts import render, redirect
# from django.urls import reverse
# # from django.views import View
# from oscar.apps.checkout.views import PaymentDetailsView
# from .forms import RazorpayPaymentForm

# class RazorpayPaymentView(PaymentDetailsView):

#     def get_context_data(self, **kwargs):
#         context = super(PaymentDetailsView, self).get_context_data(**kwargs)
#         client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))
#         order_amount = int(self.request.basket.total_incl_tax * 100)  # Amount in paise
#         order_currency = 'INR'
#         order_receipt = 'order_rcptid_11'
#         notes = {'Shipping address': 'Bommanahalli, Bangalore'}  # OPTIONAL

#         order = client.order.create({
#             'amount': order_amount,
#             'currency': order_currency,
#             'receipt': order_receipt,
#             'notes': notes
#         })
#         print(order)
#         context['razorpay_order_id'] = order['id']
#         context['razorpay_key'] = settings.RAZORPAY_PUBLISHABLE_KEY
#         context['order_amount'] = order_amount
        
#         return context

#     def post(self, request, *args, **kwargs):
#         form = RazorpayPaymentForm(request.POST)
#         if form.is_valid():
#             client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))
#             params_dict = {
#                 'razorpay_order_id': form.cleaned_data['razorpay_order_id'],
#                 'razorpay_payment_id': form.cleaned_data['razorpay_payment_id'],
#                 'razorpay_signature': form.cleaned_data['razorpay_signature']
#             }

#             try:
#                 client.utility.verify_payment_signature(params_dict)
#                 # Payment successful, handle order completion
#                 return redirect(reverse('checkout:thank-you'))
#             except razorpay.errors.SignatureVerificationError:
#                 # Payment failed, handle accordingly
#                 return redirect(reverse('checkout:payment-preview'))
#         return redirect(reverse('checkout:payment-details'))




# from django.shortcuts import redirect
# from django.urls import reverse
# from oscar.apps.checkout import views
# from oscar.apps.payment import models, exceptions
# from oscar_ecom.settings import RAZORPAY_PUBLISHABLE_KEY, RAZORPAY_API_SECRET
# import razorpay  # Razorpay's Python SDK


# from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from oscar.apps.payment.models import SourceType, Source
# from oscar.core.loading import get_model
# from . import forms
# from .facade import Facade
# from . import PAYMENT_METHOD_RAZORPAY, PAYMENT_EVENT_PURCHASE, RAZORPAY_EMAIL, RAZORPAY_TOKEN

# class PaymentDetailsView(CorePaymentDetailsView):

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
#         if self.preview:
#             ctx['razorpay_token_form'] = forms.RazorpayTokenForm(self.request.POST)
#             ctx['order_total_incl_tax_cents'] = (
#                 ctx['order_total'].incl_tax * 100
#             ).to_integral_value()
#         else:
#             ctx['order_total_incl_tax_cents'] = (
#                     ctx['order_total'].incl_tax * 100
#             ).to_integral_value()
#             ctx['razorpay_publishable_key'] = RAZORPAY_PUBLISHABLE_KEY
#         return ctx

#     def handle_payment(self, order_number, total, **kwargs):
#         razorpay_ref = Facade().charge(
#             order_number,
#             total,
#             card=self.request.POST[RAZORPAY_TOKEN],
#             description=self.payment_description(order_number, total, **kwargs),
#             metadata=self.payment_metadata(order_number, total, **kwargs))

#         source_type, __ = SourceType.objects.get_or_create(name=PAYMENT_METHOD_RAZORPAY)
#         source = Source(
#             source_type=source_type,
#             currency=OSCAR_DEFAULT_CURRENCY,
#             amount_allocated=total.incl_tax,
#             amount_debited=total.incl_tax,
#             reference=razorpay_ref)
#         self.add_payment_source(source)

#         self.add_payment_event(PAYMENT_EVENT_PURCHASE, total.incl_tax)

#     def payment_description(self, order_number, total, **kwargs):
#         return self.request.POST[RAZORPAY_EMAIL]

#     def payment_metadata(self, order_number, total, **kwargs):
#         return {'order_number': order_number}


# views.py

# import razorpay
# from oscar_ecom.settings import RAZORPAY_PUBLISHABLE_KEY, RAZORPAY_API_SECRET
# from django.shortcuts import redirect
# from django.views.decorators.csrf import csrf_exempt
# from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
# from .forms import RazorpayPaymentForm
# from oscar.apps.payment.models import SourceType, Source
# from oscar.apps.payment.exceptions import PaymentError
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from . import forms
# class PaymentDetailsView(CorePaymentDetailsView):


#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
#         if self.preview:
#             ctx['razorpay_token_form'] = forms.RazorpayPaymentForm(self.request.POST)
#             ctx['order_total_incl_tax_cents'] = (
#                 ctx['order_total'].incl_tax * 100
#             ).to_integral_value()
#         else:
#             ctx['order_total_incl_tax_cents'] = (
#                     ctx['order_total'].incl_tax * 100
#             ).to_integral_value()
#             ctx['razorpay_publishable_key'] = RAZORPAY_PUBLISHABLE_KEY
#         return ctx
#     def handle_payment(self, order_number, total, **kwargs):
#         order = self.create_order(order_number, total)
#         razorpay_ref = order['id']
#         self.add_razorpay_payment_source(order_number, total, razorpay_ref)
#         super().handle_payment(order_number, total, **kwargs)

#     def create_order(self, order_number, total):
#         client = razorpay.Client(auth=(RAZORPAY_PUBLISHABLE_KEY,RAZORPAY_API_SECRET))
#         order_data = {
#             'amount': int(total.incl_tax * 100),  # amount in paise
#             'currency': 'INR',
#             'payment_capture': '1'
#         }
#         order = client.order.create(data=order_data)
#         return order

#     def add_razorpay_payment_source(self, order_number, total, razorpay_ref):
#         source_type, __ = SourceType.objects.get_or_create(name='Razorpay')
#         source = Source(
#             source_type=source_type,
#             currency='INR',
#             amount_allocated=total.incl_tax,
#             amount_debited=total.incl_tax,
#             reference=razorpay_ref)
#         self.add_payment_source(source)
#         self.add_payment_event('Purchase', total.incl_tax)

# @csrf_exempt
# def payment_success(request):
#     form = RazorpayPaymentForm(request.POST)
#     if form.is_valid():
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         params_dict = {
#             'razorpay_order_id': form.cleaned_data['razorpay_order_id'],
#             'razorpay_payment_id': form.cleaned_data['razorpay_payment_id'],
#             'razorpay_signature': form.cleaned_data['razorpay_signature']
#         }
#         try:
#             client.utility.verify_payment_signature(params_dict)
#             # Payment successful, update order status
#             # Add your order processing logic here
#             return redirect('checkout:thank-you')
#         except razorpay.errors.SignatureVerificationError:
#             return redirect('checkout:payment-failed')
#     return redirect('checkout:payment-failed')