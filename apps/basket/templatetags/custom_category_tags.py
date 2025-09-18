from django import template
from apps.catalogue.models import Category, Product
from django.db.models import Sum

from oscar.core.loading import get_model

register = template.Library()
Category = get_model("catalogue", "category")

Product = get_model('catalogue', 'Product')


@register.simple_tag
def top_categories_with_products(limit=10, products_per_category=3):
    """
    Template tag to get top categories based on product sales,
    including a limited number of unique top products per category.
    """
    # Get top categories by total sales
    categories = Category.objects.annotate(
        total_sales=Sum('product__basket_lines__quantity')
    ).order_by('-total_sales')[:limit]

    # Include a limited number of distinct products for each category
    category_data = []
    for category in categories:
        products = (
            Product.objects.filter(categories=category)
            .annotate(total_quantity=Sum('basket_lines__quantity'))
            .distinct()
            .order_by('-total_quantity')[:products_per_category]
        )
        category_data.append({
            'category': category,
            'products': products
        })

    return category_data

