from django import forms
from django.forms.models import inlineformset_factory
from .models import SiteInfo, SocialMediaLink, MenuName, Tags

class SiteInfoForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = ['site_name','site_logo', 'site_phone', 'welcome_message', 'address', 'contact_email', 'hours_of_operation', 'whatsapp_number', 'baner1_image', 'baner2_image', 'baner3_image', 'baner4_image']

SocialMediaLinkFormSet = inlineformset_factory(SiteInfo, SocialMediaLink, fields=('platform_name',"media_logo_link", 'url'), extra=1, can_delete=True)

MenuNameFormSet = inlineformset_factory(SiteInfo, MenuName, fields=('name', 'url'), extra=1, can_delete=True)

TagsFormSet = inlineformset_factory(SiteInfo, Tags, fields=('tag_line', 'tag_link', 'tag_percentage'), extra=1, can_delete=True)
