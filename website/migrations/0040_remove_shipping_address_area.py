# Generated by Django 4.0.2 on 2022-03-04 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0039_shipping_address_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping_address',
            name='area',
        ),
    ]
