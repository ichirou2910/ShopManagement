from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart_get, name='cart_get'),
    path('viewproduct/<str:pid>/', views.product_details, name='details'),
    path('<str:pid>/', views.product_cart, name='cart'),
]
