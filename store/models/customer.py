from django.db import models

class Customer(models.Model):
    username=models.CharField(max_length=100,default='')
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    address = models.CharField(max_length=150,default='',blank=True)
    phone=models.CharField(max_length=15,default='',blank=True)
    email=models.EmailField()
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.fname


    # def register(self):
    #     self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


