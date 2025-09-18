from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from apps.catalogue.models import Brand, Product, ProductBrand

from .forms import BrandForm, ProductForm


class ProductBrandForm(forms.ModelForm):
    class Meta:
        model = ProductBrand
        fields = ['brand']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.filter(is_public=True)
        self.fields['brand'].empty_label = "Select a brand"


BaseProductBrandFormSet = inlineformset_factory(
    Product, ProductBrand, form=ProductBrandForm, extra=1, can_delete=True
)


class ProductBrandFormSet(BaseProductBrandFormSet):
    # pylint: disable=unused-argument
    def __init__(self, product_class, user, *args, **kwargs):
        # This function just exists to drop the extra arguments
        super().__init__(*args, **kwargs)

    def clean(self):
        # Allow products without brands for now - remove strict validation
        # if not self.instance.is_child and self.get_num_brands() == 0:
        #     raise forms.ValidationError(
        #         _("Stand-alone and parent products must have at least one brand")
        #     )
        if self.instance.is_child and self.get_num_brands() > 0:
            raise forms.ValidationError(_("A child product should not have brands"))

    def get_num_brands(self):
        num_brands = 0
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            if (
                hasattr(form, "cleaned_data")
                and form.cleaned_data.get("brand", None)
                and not form.cleaned_data.get("DELETE", False)
            ):
                num_brands += 1
        return num_brands