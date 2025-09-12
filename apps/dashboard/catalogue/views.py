# dashboard_catalogue/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django_tables2 import SingleTableView
from apps.catalogue.models import Brand, Product
from .formsets import ProductBrandFormSet
from .forms import BrandForm
from .tables import BrandTable
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as CoreProductCreateUpdateView


class BrandListView(SingleTableView):
    model = Brand
    table_class = BrandTable
    template_name = 'oscar/dashboard/catalogue/brand_list.html'


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'oscar/dashboard/catalogue/brand_form.html'
    success_url = reverse_lazy('dashboard:catalogue-brand-list')

class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'oscar/dashboard/catalogue/brand_form.html'
    success_url = reverse_lazy('dashboard:catalogue-brand-list')

class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'oscar/dashboard/catalogue/brand_delete.html'
    success_url = reverse_lazy('dashboard:catalogue-brand-list')


class CustomProductCreateUpdateView(CoreProductCreateUpdateView):
   
    brand_formset = ProductBrandFormSet

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formsets = {
            "category_formset": self.category_formset,
            "brand_formset": self.brand_formset,
            "image_formset": self.image_formset,
            "recommended_formset": self.recommendations_formset,
            "stockrecord_formset": self.stockrecord_formset,
        }
