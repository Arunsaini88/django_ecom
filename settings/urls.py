


from django.urls import path
from . import views

urlpatterns = [
    path('', views.SiteInfoListView.as_view(), name='site-settings-list'),
    path('manage/<int:pk>/', views.SiteInfoUpdateView.as_view(), name='manage-site-settings'),
    path('manage/', views.SiteInfoCreateView.as_view(), name='create-site-settings'),
    path('delete/<int:pk>/', views.SiteInfoDeleteView.as_view(), name='delete-site-settings'),
]
