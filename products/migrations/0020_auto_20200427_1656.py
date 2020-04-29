# Generated by Django 2.2.9 on 2020-04-27 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20200427_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product_image',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='buy_price',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(db_column='product', null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
