from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct
import uuid
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    about = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brands/logos', blank=True, null=True)
    featured_image = models.ImageField(upload_to='brands/featured_images', blank=True, null=True)
    banner = models.ImageField(upload_to='brands/banners', blank=True, null=True)
    is_public = models.BooleanField(default=False)
    brand_slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.brand_slug:
            self.brand_slug = uuid.uuid4().hex[:8]  # Generate a short unique identifier
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalogue:brand-detail', kwargs={'brand_slug': self.brand_slug, 'pk': self.pk})

class Product(AbstractProduct):
    brands = models.ManyToManyField(Brand, through='ProductBrand', related_name='products')

class ProductBrand(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

from oscar.apps.catalogue.models import *  # Ensure all other models are included
