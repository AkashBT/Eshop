from django.urls import path
from . import views
app_name='ecom'

urlpatterns = [
    
    path('',views.Home.as_view(),name="home"),
    path('register/',views.SignupSel,name="signup"),
    path('login/',views.signinseller,name='signin'),
    path('logout/',views.logouts,name='signout'),
    path('subcategory/productview/<int:pk>',views.Products.as_view(),name='product'),
    path('product/<int:pk>',views.Addproduct.as_view(),name='addproduct'),
    path('prooduct/update/<int:pk>', views.Upproduct.as_view(),name='upproduct'),
    path('prooduct/delete/<int:pk>', views.Delproduct.as_view(),name='delproduct'),
    
]