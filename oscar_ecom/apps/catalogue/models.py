from django.db import models

from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='brands', blank=True, null=True)


    def __str__(self):
        return self.name

    

from oscar.apps.catalogue.abstract_models import AbstractProduct

class Product(AbstractProduct):
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, blank=True, null=True)




from oscar.apps.catalogue.models import * 
