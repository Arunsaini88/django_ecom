from django.apps import apps
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from oscar.app import application
# from cashondelivery.dashboard.app import application as cod_app
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    path('', views.Home, name="Home"), # Home view
    path('category/', views.Category, name="Category"), # Category view
    path('brand/', views.Brand, name="brand"), # Brand view
    path('admin/', admin.site.urls),
    path('dashboard/setting/', include('settings.urls')),
    # path('dashboard/cod/', include((cod_app.urls, 'cashondelivery.dashboard'))),
    path('', include(apps.get_app_config('oscar').urls[0])),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)