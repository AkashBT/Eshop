from django.db import models
from django.db.models.base import Model
from django.db.models.fields.files import FileField
from django.urls import reverse
# Create your models here.

# model for seller
class Seller(models.Model):
    name=models.CharField(max_length=100)
    company=models.CharField(max_length=100,unique=True,help_text='Enter the company name')
    phone=models.CharField(max_length=10)
    email=models.EmailField()
    address=models.TextField(max_length=1000)
    password=models.CharField(max_length=200,default=0)
    def __str__(self):
        return f'company:{self.company} name:{self.name}'

# models for category
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    image=models.FileField()
    def __str__(self):
        return f"category:{self.name}"


# model for subcategory
class SubCategory(models.Model):
    catid=models.ForeignKey(Category,on_delete=models.CASCADE)

    name=models.CharField(max_length=100)
    image=models.FileField()
    def __str__(self):
        return f"sub-category:{self.name}"

# models for category
class Product(models.Model):
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    desc=models.TextField(max_length=1000)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.IntegerField()
    image=models.FileField()
    slid=models.ForeignKey(Seller, on_delete=models.CASCADE)
    subid=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    def __str__(self):
        return f"name:{self.name} brand:{self.brand}"
    def get_absolute_url(self):
        return reverse("ecom:home")
    

