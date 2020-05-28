from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.product_search, name='product_search'),
    path('cart/', views.cart_get, name='cart_get'),
    path('orders/', views.orders_get, name='orders_get'),
    path('viewproduct/<str:pid>/', views.product_details, name='product_details'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/delete/<str:pid>/', views.cart_delete, name="cart_delete"),
    path('orders/details/<str:oid>', views.order_details, name='order_details'),
    path('orders/cancel/<str:oid>', views.order_cancel, name='order_cancel'),
    # Fk that, stay here!
    path('<str:pid>/', views.cart_add, name='cart'),
]
