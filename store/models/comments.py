# from django.db import models

# from .product import Product
# from .customer import Customer


# class Comment(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
#     user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
#     created = models.DateField(auto_now_add=True)
#     updated = models.DateField(auto_now=True)

#     def __str__(self):
#         return self.title