from django.urls import path

from . import views

urlpatterns = [
    path('products/add/', views.product_add, name='product_add'),
    path('products/accept_add/', views.product_accept_add, name='product_accept_add'),

    # Don't move these
    path('products/<str:pid>/', views.product_change, name='product_change'),
    path('products/accept_change/<str:pid>', views.product_accept_change, name='product_accept_change'),
    path('products/delete/<str:pid>', views.product_delete, name='product_delete'),
    path('orders/change_status/<str:oid>', views.order_status_change, name='order_status_change'),
    path('orders/details/<str:oid>', views.order_details, name='order_details'),
]
