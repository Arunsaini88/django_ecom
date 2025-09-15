from django import forms
from oscar.apps.payment.models import SourceType

PAYMENT_METHOD_CHOICES = [
    ('razorpay', 'Online Payment (Razorpay)'),
    ('cod', 'Cash on Delivery (COD)'),
]

class PaymentMethodForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        initial='razorpay'
    )

class RazorpayPaymentForm(forms.Form):
    razorpay_payment_id = forms.CharField()
    razorpay_order_id = forms.CharField()
    razorpay_signature = forms.CharField(required=False)