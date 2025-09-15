import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext_lazy

from django.utils.translation import gettext_lazy as _
from django_tables2.utils import A
from apps.catalogue.models import Brand

class BrandTable(tables.Table):
    name = tables.LinkColumn("dashboard:catalogue-brand-update", args=[A("pk")])
    description = tables.TemplateColumn(
        template_code='{{ record.description|default:""|striptags|truncatewords:6 }}'
    )
    actions = tables.TemplateColumn(
        template_name="oscar/dashboard/catalogue/brand_row_actions.html",
        orderable=False,
    )

    icon = "sitemap"
    caption = ngettext_lazy("%s Brand", "%s Brands")
    
    class Meta:
        model = Brand
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "description",  "slug", "is_public", "actions")