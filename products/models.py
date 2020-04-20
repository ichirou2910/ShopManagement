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
    product_image = models.CharField(db_column='productImage', max_length=100)  # Field name made lowercase.
    company = models.CharField(max_length=25)
    product_description = models.TextField(db_column='productDescription')  # Field name made lowercase.
    quantity_in_stock = models.SmallIntegerField(db_column='quantityInStock')  # Field name made lowercase.
    sell_price = models.IntegerField(db_column='sellPrice')  # Field name made lowercase.
    buy_price = models.IntegerField(db_column='buyPrice')  # Field name made lowercase.

    class Meta:
        db_table = 'products'
