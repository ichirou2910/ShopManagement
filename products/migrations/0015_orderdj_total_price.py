# Generated by Django 2.2.9 on 2020-04-27 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20200427_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdj',
            name='total_price',
            field=models.IntegerField(db_column='totalPrice', default=0),
        ),
    ]