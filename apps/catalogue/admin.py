
from oscar.apps.catalogue.admin import *  # Import everything from the default admin
from .models import Brand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_slug')
    prepopulated_fields = {'brand_slug': ('name',)}
