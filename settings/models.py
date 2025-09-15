from django.db import models

class SiteInfo(models.Model):
    site_name = models.CharField(max_length=100, blank=True, null=True)
    site_logo = models.ImageField(upload_to='site_logo/', null=True, blank=True)
    site_phone = models.CharField(max_length=20, blank=True, null=True)
    welcome_message = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=300,blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    hours_of_operation = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    baner1_image = models.ImageField(upload_to='baner_image/', null=True, blank=True)
    baner2_image = models.ImageField(upload_to='baner_image/', null=True, blank=True)
    baner3_image = models.ImageField(upload_to='baner_image/', null=True, blank=True)
    baner4_image = models.ImageField(upload_to='baner_image/', null=True, blank=True)
    brand_baner_image = models.ImageField(upload_to='baner_image/', null=True, blank=True)
    category_baner_image = models.ImageField(upload_to='baner_image/', null=True, blank=True)

    def __str__(self):
        return "Site Settings"

class SocialMediaLink(models.Model):
    settings = models.ForeignKey(SiteInfo, related_name='social_links', on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=100,blank=True, null=True)
    media_logo_link = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.platform_name}: {self.url}"

class MenuName(models.Model):
    settings = models.ForeignKey(SiteInfo, related_name='menu_names', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.url}"

class Tags(models.Model):
    settings = models.ForeignKey(SiteInfo, related_name='tags', on_delete=models.CASCADE)
    tag_line = models.CharField(max_length=250,blank=True, null=True)
    tag_link = models.URLField(blank=True, null=True)
    tag_percentage = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tag_description}: {self.tag_link}"