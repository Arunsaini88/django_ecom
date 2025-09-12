from django import forms
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm
from apps.catalogue.models import Product, Brand  # Import your custom Product model

class ProductForm(CoreProductForm):
    brands = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)

    class Meta(CoreProductForm.Meta):
        model = Product
        fields = CoreProductForm.Meta.fields + ['brands']  # Add 'brand' to the fields


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"