from django.conf import settings
from django.utils.module_loading import import_string
from django.views.generic.list import MultipleObjectMixin

from oscar.core.loading import get_class, get_classes, get_model

BrowseCategoryForm = get_class("search.forms", "BrowseCategoryForm")
BrowseBrandForm = get_class("search.forms", "BrowseBrandForm")

SearchHandler, SearchResultsPaginationMixin = get_classes(
    "search.search_handlers", ("SearchHandler", "SearchResultsPaginationMixin")
)
is_solr_supported = get_class("search.features", "is_solr_supported")
is_elasticsearch_supported = get_class("search.features", "is_elasticsearch_supported")
Product = get_model("catalogue", "Product")


def get_product_search_handler_class():
    """
    Determine the search handler to use.

    Currently only Solr is supported as a search backend, so it falls
    back to rudimentary category browsing if that isn't enabled.
    """
    # Use get_class to ensure overridability
    if settings.OSCAR_PRODUCT_SEARCH_HANDLER is not None:
        return import_string(settings.OSCAR_PRODUCT_SEARCH_HANDLER)
    if is_solr_supported():
        return get_class("catalogue.search_handlers", "SolrProductSearchHandler")
    elif is_elasticsearch_supported():
        return get_class(
            "catalogue.search_handlers",
            "ESProductSearchHandler",
        )
    else:
        return get_class("catalogue.search_handlers", "SimpleProductSearchHandler")


class SolrProductSearchHandler(SearchHandler):
    """
    Search handler specialised for searching products.  Comes with optional
    category and brand filtering. To be used with a Solr search backend.
    """

    form_class = BrowseCategoryForm
    brand_form_class = BrowseBrandForm
    model_whitelist = [Product]
    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    def __init__(self, request_data, full_path, product_per_page=None, categories=None, brands=None):
        self.categories = categories
        self.brands = brands
        self.paginate_by = product_per_page or settings.OSCAR_PRODUCTS_PER_PAGE
        super().__init__(request_data, full_path)

    def get_search_queryset(self):
        sqs = super().get_search_queryset()
        if self.categories:
            pattern = " OR ".join(
                ['"%s"' % sqs.query.clean(c.full_name) for c in self.categories]
            )
            sqs = sqs.narrow("category_exact:(%s)" % pattern)
        if self.brands:
            pattern = " OR ".join(
                ['"%s"' % sqs.query.clean(b.name) for b in self.brands]
            )
            sqs = sqs.narrow("brand_exact:(%s)" % pattern)
        return sqs


class ESProductSearchHandler(SearchHandler):
    """
    Search handler specialised for searching products.  Comes with optional
    category and brand filtering. To be used with an ElasticSearch search backend.
    """

    form_class = BrowseCategoryForm
    brand_form_class = BrowseBrandForm
    model_whitelist = [Product]
    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    def __init__(self, request_data, full_path, categories=None, brands=None):
        self.categories = categories
        self.brands = brands
        super().__init__(request_data, full_path)

    def get_search_queryset(self):
        sqs = super().get_search_queryset()
        if self.categories:
            for category in self.categories:
                sqs = sqs.filter_or(category=category.full_name)
        if self.brands:
            for brand in self.brands:
                sqs = sqs.filter_or(brand=brand.name)
        return sqs


class SimpleProductSearchHandler(SearchResultsPaginationMixin, MultipleObjectMixin):
    """
    A basic implementation of the full-featured SearchHandler that has no
    faceting support, but doesn't require a Haystack backend. It only
    supports category and brand browsing.

    Note that is meant as a replacement search handler and not as a view
    mixin; the mixin just does most of what we need it to do.
    """

    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    def __init__(self, request_data, full_path, categories=None, brands=None):
        self.request_data = request_data
        self.categories = categories
        self.brands = brands
        self.kwargs = {"page": request_data.get("page") or 1}
        self.object_list = self.get_queryset()

    def get_queryset(self):
        qs = Product.objects.browsable().base_queryset()
        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()
        if self.brands:
            qs = qs.filter(brands__in=self.brands).distinct()
        return qs

    def get_search_context_data(self, context_object_name):
        self.context_object_name = context_object_name
        context = self.get_context_data(object_list=self.object_list)
        context[context_object_name] = context["page_obj"].object_list
        return context
