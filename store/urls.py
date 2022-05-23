from django.contrib import admin
from django.urls import path
from .views import Index,signup,Login,logout,Carts,OrderView,category,success,read_all,add_wishlist,wishlist,removewishlist,search,invoice,popup,dashboard
from .middlewares.auth import auth_middleware

app_name='store'




urlpatterns = [

    path('',Index.as_view(),name="index"),
    path('signup/',signup,name="signup"),
    path('signin/',Login.as_view(),name="signin"),
    path('carts/',Carts.as_view(),name="cart"),
    path('logout/',logout,name="logout"),
    path('dashboard/',dashboard,name='dashboard'),


    path('orders/',auth_middleware(OrderView.as_view()),name="orders"),
    path('success/',success,name="success"),

    path('read_all/<int:pk>',read_all,name="read_all"),
    path('wishlist/',wishlist,name='wishlist'),
    path('add_wishlist/<int:pk>',add_wishlist,name='add_wishlist'),
    path('removewishlist/<int:pk>',removewishlist,name='removewishlist'),

    path('category/<int:pk>',category,name='category'),

    path('search/',search,name='search'),

    path('invoice/<int:pk>',invoice,name="invoice"),

    path('popup',popup,name="popup"),


]
