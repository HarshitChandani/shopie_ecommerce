# Generated by Django 4.0.2 on 2022-03-01 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0031_remove_product_orderdetails_item_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_orderdetails',
            name='SP',
            field=models.IntegerField(default=0, verbose_name='S.P(Selling Price)'),
        ),
    ]
