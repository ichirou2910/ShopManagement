# Generated by Django 2.2.9 on 2020-04-27 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20200427_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(db_column='product', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pd', to='products.Product'),
        ),
    ]