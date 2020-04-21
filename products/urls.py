from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('viewproduct/<str:pid>/', views.product_details, name='details'),
    path('inform/<str:pid>/', views.product_cart, name='cart')
]
