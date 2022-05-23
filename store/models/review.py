from django.db import models

from .product import Product
from .customer import Customer


class Review(models.Model):
    review = models.TextField()
    product = models.CharField(max_length=10)
    user = models.CharField(max_length=10)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

