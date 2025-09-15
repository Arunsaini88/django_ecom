from urllib import parse

from django import template
from django.urls import Resolver404, resolve
from django.utils.translation import gettext_lazy as _

from oscar.core.loading import get_class, get_model

Site = get_model("sites", "Site")
CustomerHistoryManager = get_class("customer.history", "CustomerHistoryManager")

register = template.Library()


@register.inclusion_tag(
    "oscar/customer/history/recently_viewed_products_home.html", takes_context=True
)
def home_recently_viewed_products(context, current_product=None):
    """
    Inclusion tag listing the most recently viewed products
    """
    request = context["request"]
    products = CustomerHistoryManager.get(request)
    if current_product:
        products = [p for p in products if p != current_product]
    return {"products": products, "request": request}
