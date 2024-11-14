from django.db import models

class SiteInfo(models.Model):
    site_logo = models.ImageField(upload_to='site_logo/', null=True, blank=True)
    site_phone = models.CharField(max_length=20, blank=True, null=True)
    welcome_message = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=300,blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    hours_of_operation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "Site Settings"

class SocialMediaLink(models.Model):
    settings = models.ForeignKey(SiteInfo, related_name='social_links', on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=100,blank=True, null=True)
    media_logo_link = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.platform_name}: {self.url}"
