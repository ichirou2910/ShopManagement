# Generated by Django 2.2.9 on 2020-04-27 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_orderdj_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdj',
            name='address',
            field=models.CharField(db_column='address', default='nonexistent', max_length=100),
        ),
    ]
