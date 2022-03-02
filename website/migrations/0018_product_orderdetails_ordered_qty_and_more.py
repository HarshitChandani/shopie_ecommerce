# Generated by Django 4.0.2 on 2022-02-28 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_product_orderdetails_discount_amt'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_orderdetails',
            name='ordered_qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product_orderdetails',
            name='ordered_size',
            field=models.IntegerField(default=32),
        ),
        migrations.AddField(
            model_name='product_orderdetails',
            name='product_slug',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.product'),
        ),
    ]