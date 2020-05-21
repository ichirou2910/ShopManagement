from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('cart/', views.cart_get, name='cart_get'),
    path('orders/', views.orders, name='order'),
    path('viewproduct/<str:pid>/', views.product_details, name='details'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/<str:pid>/', views.delete_cart, name="delete"),
    # Fk that, stay here!
    path('<str:pid>/', views.product_cart, name='cart'),
]
