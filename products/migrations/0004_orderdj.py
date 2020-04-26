# Generated by Django 2.2.9 on 2020-04-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200424_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDJ',
            fields=[
                ('order_id', models.AutoField(db_column='orderID', primary_key=True, serialize=False)),
                ('product_id', models.CharField(db_column='productID', max_length=10)),
                ('user', models.CharField(db_column='user', max_length=25)),
                ('product_name', models.CharField(db_column='productName', max_length=25)),
                ('quantity', models.IntegerField(db_column='quantity')),
                ('price', models.IntegerField(db_column='sellPrice')),
            ],
            options={
                'db_table': 'orderDJ',
            },
        ),
    ]
