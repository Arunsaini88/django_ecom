from django import forms
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm
from apps.catalogue.models import Product, Brand, ProductBrand

class ProductForm(CoreProductForm):
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.filter(is_public=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select one or more brands for this product"
    )

    class Meta(CoreProductForm.Meta):
        model = Product
        fields = CoreProductForm.Meta.fields  # Don't add 'brands' to fields since it's handled specially
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # If editing existing product, pre-select associated brands
            self.fields['brands'].initial = self.instance.brands.all()
    
    def save(self, commit=True):
        product = super().save(commit=commit)
        if commit:
            # Clear existing brand relationships
            ProductBrand.objects.filter(product=product).delete()
            
            # Create new brand relationships
            for brand in self.cleaned_data['brands']:
                ProductBrand.objects.create(product=product, brand=brand)
        
        return product


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"