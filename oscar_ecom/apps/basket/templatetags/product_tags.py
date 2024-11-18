from django import template
from django.template.loader import select_template
from oscar.apps.order.models import Line
from django.db.models import Sum, Q
from django.db.models import Count
from oscar.apps.analytics.models import UserProductView
from apps.catalogue.models import Product

register = template.Library()


# your_project/templatetags/product_tags.py


@register.simple_tag
def get_top_rated_products(limit=5):
    # Assumes a rating field exists on the Product model
    return Product.objects.filter(rating__isnull=False).order_by('-rating')[:limit]



@register.simple_tag
def newest_products(limit=5):
    return  Product.objects.filter(is_public=True).order_by('-date_created')[:limit]



@register.simple_tag
def best_selling_products(limit=5):
    return (
        Product.objects
        .annotate(num_sales=Count('line'))
        .order_by('-num_sales')[:limit]
    )


@register.simple_tag
def most_popular_products(limit=5):
    # Get the most viewed products based on user views
    popular_products = (
        Product.objects
        .annotate(num_views=Count('userproductview'))  # Count views
        .order_by('-num_views')[:limit]  # Limit to top 10 most viewed
    )
    return popular_products


@register.simple_tag
def all_products(limit=10):
    return Product.objects.all()[0:limit]



@register.inclusion_tag('custom_temps/product_detail/related_product.html', takes_context=True)
def related_products(context, product):
    # Fetch products from the same category (or any other criteria)
    request = context["request"]
    
    products = Product.objects.filter(
        categories__in=product.categories.all()
    ).exclude(id=product.id)

    return {'products': products, "request": request}