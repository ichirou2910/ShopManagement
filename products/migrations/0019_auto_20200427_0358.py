# Generated by Django 2.2.9 on 2020-04-27 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20200427_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdj',
            name='phone_number',
            field=models.CharField(db_column='phoneNumber', default='0000000000', max_length=15),
        ),
        migrations.AddField(
            model_name='orderdj',
            name='user',
            field=models.CharField(db_column='user', default='noname', max_length=25),
        ),
    ]
