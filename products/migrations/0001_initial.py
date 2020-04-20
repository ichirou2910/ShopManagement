# Generated by Django 2.2.9 on 2020-04-20 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('productid', models.CharField(db_column='productID', max_length=10, primary_key=True, serialize=False)),
                ('productname', models.CharField(db_column='productName', max_length=25)),
                ('productimage', models.CharField(db_column='productImage', max_length=100)),
                ('company', models.CharField(max_length=25)),
                ('productdescription', models.TextField(db_column='productDescription')),
                ('quantityinstock', models.SmallIntegerField(db_column='quantityInStock')),
                ('sellprice', models.IntegerField(db_column='sellPrice')),
                ('buyprice', models.IntegerField(db_column='buyPrice')),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
