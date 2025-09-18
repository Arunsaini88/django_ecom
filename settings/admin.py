from django.contrib import admin
from .models import SiteInfo, SocialMediaLink
# Register your models here.
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_phone_number', 'welcome_message')
    filter_horizontal = ('social_links',)

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'url')