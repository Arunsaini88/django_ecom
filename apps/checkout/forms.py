from django import forms
from oscar.apps.payment.models import SourceType

class PaymentMethodForm(forms.Form):
    payment_method = forms.ModelChoiceField(queryset=SourceType.objects.all(), empty_label=None)

class RazorpayPaymentForm(forms.Form):
    razorpay_payment_id = forms.CharField()
    razorpay_order_id = forms.CharField()
    razorpay_signature = forms.CharField()