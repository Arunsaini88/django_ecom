from django import forms
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm
from catalogue.models import Product, Brand  # Import your custom Product model

class ProductForm(CoreProductForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)

    class Meta(CoreProductForm.Meta):
        model = Product
        fields = CoreProductForm.Meta.fields + ['brand']  # Add 'brand' to the fields
