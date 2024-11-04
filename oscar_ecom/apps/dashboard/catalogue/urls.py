# dashboard_catalogue/urls.py

from django.urls import path
from . import views

app_name = 'dashboard_catalogue'

urlpatterns = [
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('brands/add/', views.BrandCreateView.as_view(), name='brand-add'),
    path('brands/<int:pk>/edit/', views.BrandUpdateView.as_view(), name='brand-edit'),
    path('brands/<int:pk>/delete/', views.BrandDeleteView.as_view(), name='brand-delete'),
]
