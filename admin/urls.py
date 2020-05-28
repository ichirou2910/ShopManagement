from django.urls import path

from . import views

urlpatterns = [
    path('products/add/', views.product_add, name='product_add'),
    path('products/accept_add/', views.product_accept_add, name='product_accept_add'),

    # Don't move these
    path('products/<str:pid>/', views.product_change, name='product_change'),
    path('products/accept_change/<str:pid>', views.product_accept_change, name='product_accept_change'),
    path('orders/change_status/<str:oid>', views.status_change, name='status_change'),
    path('orders/details/<str:oid>', views.details, name='details'),
]
