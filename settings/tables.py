import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext_lazy

from django.utils.translation import gettext_lazy as _
from django_tables2.utils import A
from settings.models import SiteInfo, SocialMediaLink

class SiteInfoTable(tables.Table):
    address = tables.TemplateColumn(
        template_code='{{ record.address|default:""|striptags|truncatewords:6 }}'
    )
    actions = tables.TemplateColumn(
        template_name="oscar/dashboard/settings/setting_row_action.html",
        orderable=False,
    )

    icon = "sitemap"
    caption = ngettext_lazy("%s Setting", "%s Settings")
    
    class Meta:
        model = SiteInfo
        template_name = "django_tables2/bootstrap.html"
        fields = ("site_phone", "address", "welcome_message" ,"contact_email", "actions")