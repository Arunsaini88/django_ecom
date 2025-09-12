import oscar.apps.catalogue.apps as apps
from django.urls import path, re_path
from oscar.core.loading import get_class
from django.utils.translation import gettext_lazy as _



class CatalogueConfig(apps.CatalogueConfig):
    name = 'apps.catalogue'

    label = "catalogue"
    verbose_name = _("Catalogue")

    namespace = "catalogue"
    def ready(self):
        super().ready()
        from .views import quick_view

        self.brand_view = get_class("catalogue.views", "BrandDetailView")
        self.quick_view = quick_view

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            re_path(
            r"^brand/(?P<brand_slug>[\w-]+)_(?P<pk>\d+)/$",
            self.brand_view.as_view(),
            name="brand-detail",
        ),
        path('quick_view/<int:pk>/',self.quick_view, name="quick_view"), # Quick view
        ]
        return self.post_process_urls(urls)