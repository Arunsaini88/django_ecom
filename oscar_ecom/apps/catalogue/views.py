from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from oscar.core.loading import get_class, get_model
from django.core.paginator import InvalidPage
from urllib.parse import quote
from django.views.generic import View
from django.template.loader import render_to_string
from django.http import HttpResponsePermanentRedirect, JsonResponse


Brand = get_model("catalogue", "Brand")
Product = get_model("catalogue", "Product")
get_product_search_handler_class = get_class("catalogue.search_handlers", "get_product_search_handler_class")


def quick_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    stockrecord = product.stockrecords.first()  # Get the first stock record
    price = stockrecord.price if stockrecord else None
    html = render_to_string('custome_temps/homepage_detail/quick_view.html', {'product': product, 'price': price}, request=request)
    return JsonResponse({'html': html})


class BrandDetailView(TemplateView):
    template_name = "oscar/catalogue/brand.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = get_object_or_404(Brand, pk=kwargs['pk'])
        products = Product.objects.filter(brands=brand)
        context['brand'] = brand
        context['products'] = products
        return context