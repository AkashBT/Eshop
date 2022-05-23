from django.db import models
from .product import Product
from .customer import Customer
import datetime


class Wishlist(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)


    def __str__(self):
        return self.product.name
