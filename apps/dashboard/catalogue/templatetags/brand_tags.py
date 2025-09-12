from django import template
from django.db.models import Count, Avg
from apps.catalogue.models import Brand, Product

register = template.Library()

@register.simple_tag
def get_brands_with_products(limit=10):
    brands = Brand.objects.annotate(num_products=Count('products'),average_rating=Avg('products__reviews__score')).order_by('-num_products')[:limit]
    # brands = Brand.objects.prefetch_related('products').all()
    return brands

@register.simple_tag
def get_same_brand_products(product, limit=10):
    brand = product.brands.first()  # Assuming a product has one brand
    if brand:
        return Product.objects.filter(brands=brand).exclude(id=product.id)[:limit]
    return Product.objects.none()


@register.simple_tag
def get_brand_logos(limit=10):
    brands = Brand.objects.filter(logo__isnull=False).distinct().order_by('name')[:limit]
    return brands
