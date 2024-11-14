from django import forms
from django.forms.models import inlineformset_factory
from .models import SiteInfo, SocialMediaLink

class SiteInfoForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = ['site_logo', 'site_phone', 'welcome_message', 'address', 'contact_email', 'hours_of_operation']

SocialMediaLinkFormSet = inlineformset_factory(SiteInfo, SocialMediaLink, fields=('platform_name',"media_logo_link", 'url'), extra=3, can_delete=True)
