# Generated by Django 4.0.2 on 2022-03-02 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0034_shipping_address_landmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping_address',
            name='area',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
