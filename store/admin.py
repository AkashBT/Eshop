from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.payment import PaymentDetails
from .models.coupon import Coupon
# from .models.comments import Comment
from .models.review import Review
from .models.wishlist import Wishlist
# Register your models here.


class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category']
admin.site.register(Product,AdminProduct)



class AdminCatrgory(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,AdminCatrgory)



class AdminCustomer(admin.ModelAdmin):
    list_display=['fname']
admin.site.register(Customer,AdminCustomer)


class AdminOrder(admin.ModelAdmin):
    list_display=['product','customer','quantity','price','date']
admin.site.register(Order,AdminOrder)

class AdminPaymentDetails(admin.ModelAdmin):
    list_display=['product','customer','quantity','price','date']
admin.site.register(PaymentDetails,AdminPaymentDetails)


class AdminCouponDetails(admin.ModelAdmin):
    list_display=['couponname']
admin.site.register(Coupon,AdminCouponDetails)



class AdminReviewDetails(admin.ModelAdmin):
    list_display=['review','product','user']
admin.site.register(Review,AdminReviewDetails)

class AdminWishlistDetails(admin.ModelAdmin):
    list_display=['product','customer']
admin.site.register(Wishlist,AdminWishlistDetails)