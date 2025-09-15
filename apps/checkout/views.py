from oscar.apps.checkout import views
from oscar.apps.payment import models
from oscar.apps.payment.exceptions import PaymentError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from oscar.apps.payment.models import Source, SourceType
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from oscar.apps.order.utils import OrderCreator


import razorpay  # Razorpay SDK for API interaction
from razorpay.errors import BadRequestError, ServerError

from django.http import JsonResponse, HttpResponse


# No custom monkey patch needed - Oscar's standard fields work fine now


class PaymentDetailsView(views.PaymentDetailsView):
    """Custom payment details view with proper order creation"""

    def dispatch(self, request, *args, **kwargs):
        return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Pass payment method options and Razorpay-specific data to the template.
        """
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        
        # Get selected payment method from session or default to Razorpay
        payment_method = self.request.session.get('payment_method', 'razorpay')
        ctx['payment_method'] = payment_method
        
        if payment_method == 'razorpay':
            try:
                client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))

                # Generate Razorpay order
                order_number = self.generate_order_number(self.request.basket)
                amount_in_paise = int(ctx['order_total'].incl_tax * 100)
                
                
                razorpay_order = client.order.create({
                    "amount": amount_in_paise,  # Amount in paise
                    "currency": "INR",
                    "receipt": str(order_number),
                    "payment_capture": 1
                })
                

                # Add Razorpay details to the context
                ctx['razorpay_key'] = settings.RAZORPAY_PUBLISHABLE_KEY
                ctx['razorpay_order_id'] = razorpay_order['id']
                ctx['basket_total'] = amount_in_paise
                ctx['order_number'] = order_number
                ctx['user_email'] = self.request.user.email if self.request.user.is_authenticated else ''
                
            except Exception as e:
                # Fall back to COD if Razorpay fails
                payment_method = 'cod'
                self.request.session['payment_method'] = payment_method
                ctx['payment_method'] = payment_method
        
        return ctx
    
    def post(self, request, *args, **kwargs):
        """Handle payment method selection and order placement"""
        
        # Check if we're on the preview page (not payment-details page)
        if 'preview' in request.path:
            # On preview page, let Oscar handle the final order placement
            return super().post(request, *args, **kwargs)
        
        # Handle order placement from payment-details page
        if 'action' in request.POST and request.POST['action'] == 'place_order':
            
            # Check if user is authenticated or allow guest checkout
            if not request.user.is_authenticated:
                # For guest checkout, ensure we have the session data
                if not hasattr(request, 'basket') or not request.basket.id:
                    messages.error(request, _("Your session has expired. Please try again."))
                    return redirect('checkout:index')
            
            return self.process_payment_and_place_order(request)
        
        # Handle payment method selection (only if not placing order)
        if 'payment_method' in request.POST and 'action' not in request.POST:
            payment_method = request.POST.get('payment_method')
            request.session['payment_method'] = payment_method
            return redirect('checkout:payment-details')
        
        return super().post(request, *args, **kwargs)
    
    def process_payment_and_place_order(self, request):
        """Process payment and place order"""
        try:
            
            # Get payment method and details
            payment_method = request.session.get('payment_method', 'razorpay')
            
            # Generate order number
            order_number = self.generate_order_number(request.basket)
            
            # For COD, we can skip complex payment processing and go straight to order creation
            if payment_method == 'cod':
                
                # Get shipping information from session (already set in previous checkout steps)
                shipping_address = self.get_shipping_address(request.basket)
                shipping_method = self.get_shipping_method(request.basket, shipping_address)
                
                # Calculate shipping charge using the shipping method
                shipping_charge = shipping_method.calculate(request.basket)
                
                
                # Handle COD payment
                self.handle_payment(
                    order_number, 
                    self.get_order_totals(request.basket, shipping_charge)
                )
                
                # For COD, redirect to preview page instead of directly placing order
                return redirect('checkout:preview')
                
            elif payment_method == 'razorpay':
                # Handle Razorpay payment
                razorpay_payment_id = request.POST.get('razorpay_payment_id')
                razorpay_order_id = request.POST.get('razorpay_order_id')  
                razorpay_signature = request.POST.get('razorpay_signature')
                
                
                if not razorpay_payment_id:
                    # This is the initial order creation from payment details page, not payment completion
                    # Just redirect to preview page without processing payment yet
                    return redirect('checkout:preview')
                
                # Payment ID exists - this is payment completion, process the payment
                
                # Get shipping information needed for order totals
                shipping_address = self.get_shipping_address(request.basket)
                shipping_method = self.get_shipping_method(request.basket, shipping_address)
                shipping_charge = shipping_method.calculate(request.basket)
                
                self.handle_payment(
                    order_number, 
                    self.get_order_totals(request.basket, shipping_charge),
                    razorpay_payment_id=razorpay_payment_id,
                    razorpay_order_id=razorpay_order_id,
                    razorpay_signature=razorpay_signature
                )
                
                # For Razorpay, redirect to preview page after successful payment
                return redirect('checkout:preview')
            
        except PaymentError as e:
            messages.error(request, str(e))
            return redirect('checkout:payment-details')
        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.error(request, _("An error occurred while processing your order. Please try again."))
            return redirect('checkout:payment-details')
    
    def place_order_helper(self, order_number):
        """Helper to place the order using Oscar's order creator"""
        order_creator = OrderCreator()
        
        basket = self.request.basket
        shipping_address = self.get_shipping_address(basket)
        shipping_method = self.get_shipping_method(basket, shipping_address)
        billing_address = self.get_billing_address(shipping_address)
        
        order_total = self.get_order_totals(basket)
        
        order = order_creator.place_order(
            basket=basket,
            total=order_total,
            shipping_method=shipping_method,
            shipping_address=shipping_address,
            billing_address=billing_address,
            order_number=order_number,
            user=self.request.user if self.request.user.is_authenticated else None,
        )
        
        # Clear the basket
        basket.flush()
        
        return order

    def handle_payment(self, order_number, total, **kwargs):
        """
        Handle payment based on selected payment method (Razorpay or COD).
        """
        payment_method = self.request.session.get('payment_method', 'razorpay')
        
        if payment_method == 'razorpay':
            self._handle_razorpay_payment(order_number, total, **kwargs)
        elif payment_method == 'cod':
            self._handle_cod_payment(order_number, total, **kwargs)
        else:
            raise PaymentError("Invalid payment method selected")
    
    def _handle_razorpay_payment(self, order_number, total, **kwargs):
        """Handle Razorpay payment validation"""
        razorpay_payment_id = kwargs.get('razorpay_payment_id')
        razorpay_order_id = kwargs.get('razorpay_order_id')
        razorpay_signature = kwargs.get('razorpay_signature')
        
        
        # Check if payment has already been processed (preview page scenario)
        # Look for existing payment in session or skip validation if on preview page
        if 'preview' in self.request.path:
            # We're on preview page, check if payment was already processed
            payment_completed = self.request.session.get('razorpay_payment_completed', False)
            if payment_completed:
                return
            # If no payment completion flag but we're on preview, something went wrong
        
        if not razorpay_payment_id:
            raise PaymentError("Razorpay payment ID is required but not provided")

        client = razorpay.Client(auth=(settings.RAZORPAY_PUBLISHABLE_KEY, settings.RAZORPAY_API_SECRET))

        try:
            # Verify payment signature for security (if available)
            if razorpay_order_id and razorpay_signature:
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                }
                client.utility.verify_payment_signature(params_dict)
            else:
                pass
            
            # Verify the payment status
            payment = client.payment.fetch(razorpay_payment_id)
            
            if payment['status'] not in ['captured', 'authorized']:
                raise PaymentError(f"Payment not successful. Status: {payment['status']}")

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
            
            # Mark payment as completed in session for preview page
            self.request.session['razorpay_payment_completed'] = True

        except razorpay.errors.SignatureVerificationError as e:
            raise PaymentError("Payment signature verification failed. This may be a fraudulent transaction.")
        except (BadRequestError, ServerError) as e:
            raise PaymentError(f"Razorpay API error: {e}")
        except Exception as e:
            raise PaymentError(f"Unexpected error during Razorpay payment handling: {e}")
    
    def _handle_cod_payment(self, order_number, total, **kwargs):
        """Handle Cash on Delivery payment"""
        try:
            # Check if payment has already been processed (preview page scenario)
            if 'preview' in self.request.path:
                payment_completed = self.request.session.get('cod_payment_completed', False)
                if payment_completed:
                    return
            
            # Record payment source for COD
            source_type, __ = models.SourceType.objects.get_or_create(name="Cash on Delivery")
            source = models.Source(
                source_type=source_type,
                amount_allocated=total.incl_tax,
                reference=f"COD-{order_number}"
            )
            self.add_payment_source(source)

            # Record payment event as deferred (will be collected on delivery)
            self.add_payment_event('deferred', total.incl_tax)
            
            # Mark COD payment as completed in session for preview page
            self.request.session['cod_payment_completed'] = True

        except Exception as e:
            raise PaymentError(f"Error processing COD payment: {e}")

