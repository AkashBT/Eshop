from django.db import models
from store.models.product import Product
class Coupon(models.Model):
    couponname = models.CharField(max_length=10,null=True)
    reduceamount=models.IntegerField(default=0)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


    def __str__(self):
        return self.couponname
