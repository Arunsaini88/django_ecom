# dashboard_catalogue/views.py

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from catalogue.models import Brand

class BrandListView(ListView):
    model = Brand
    template_name = 'dashboard/catalogue/brand_list.html'

class BrandCreateView(CreateView):
    model = Brand
    fields = ['name', 'description']
    template_name = 'dashboard/catalogue/brand_form.html'
    success_url = reverse_lazy('dashboard:brand-list')

class BrandUpdateView(UpdateView):
    model = Brand
    fields = ['name', 'description']
    template_name = 'dashboard/catalogue/brand_form.html'
    success_url = reverse_lazy('dashboard:brand-list')

class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'dashboard/catalogue/brand_confirm_delete.html'
    success_url = reverse_lazy('dashboard:brand-list')
