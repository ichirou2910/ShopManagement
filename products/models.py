# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Product(models.Model):
    product_id = models.CharField(db_column='productID', primary_key=True, max_length=10)  # Field name made lowercase.
    product_name = models.CharField(db_column='productName', max_length=25)  # Field name made lowercase.
    product_image = models.CharField(db_column='productImage', max_length=100, blank=True)  # Field name made lowercase.
    company = models.CharField(max_length=25)
    product_description = models.TextField(db_column='productDescription')  # Field name made lowercase.
    quantity_in_stock = models.IntegerField(db_column='quantityInStock')  # Field name made lowercase.
    sell_price = models.IntegerField(db_column='sellPrice')  # Field name made lowercase.

    class Meta:
        db_table = 'products'


class Cart(models.Model):
    ord = models.AutoField(db_column='ord', primary_key=True)
    quantity = models.IntegerField(db_column='quantity')
    user = models.CharField(db_column='user', max_length=25)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cart'


class Orders(models.Model):
    order_id = models.AutoField(db_column='orderID', primary_key=True)
    user = models.CharField(db_column='user', default='noname', max_length=25)
    customer_name = models.CharField(db_column='customerName', default='noname', max_length=25)
    address = models.CharField(db_column='address', default='nonexistent', max_length=100)
    phone_number = models.CharField(db_column='phoneNumber', default='0000000000', max_length=15)
    total_price = models.IntegerField(db_column='totalPrice', default=0)
    status = models.CharField(db_column='status', max_length=10, default='Pending')

    class Meta:
        db_table = 'orders'


class OrderDetails(models.Model):
    order_id = models.ForeignKey('Orders', on_delete=models.CASCADE, db_column='order_id')
    user = models.CharField(db_column='user', max_length=25)
    quantity = models.IntegerField(db_column='quantity')
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = (('order_id', 'product_id'),)
        db_table = 'orderdetails'
