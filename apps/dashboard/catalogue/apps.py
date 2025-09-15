import oscar.apps.dashboard.catalogue.apps as apps
from oscar.core.loading import get_class
from django.urls import path



class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    name = 'apps.dashboard.catalogue'

    def ready(self):
        super().ready()
        from .views import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView, CustomProductCreateUpdateView

        # Brand views
        self.brand_list_view = BrandListView
        self.brand_create_view = BrandCreateView
        self.brand_update_view = BrandUpdateView
        self.brand_delete_view = BrandDeleteView
        
        # Override the main product create/update view to include brand support
        self.product_createupdate_view = CustomProductCreateUpdateView


    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('brand/', self.brand_list_view.as_view(), name='catalogue-brand-list'),
            path('brand/create/', self.brand_create_view.as_view(), name='catalogue-brand-create'),
            path('brand/<int:pk>/update/', self.brand_update_view.as_view(), name='catalogue-brand-update'),
            path('brand/<int:pk>/delete/', self.brand_delete_view.as_view(), name='catalogue-brand-delete'),
        ]
        return self.post_process_urls(urls)