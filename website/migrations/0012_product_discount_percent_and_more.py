# Generated by Django 4.0.2 on 2022-02-25 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_pattern_title_alter_product_fabric_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='is_discount_applicable',
            field=models.BooleanField(default=False, help_text='Check If this product is in discount scheme and discount percent will be auto calculated.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='MRP',
            field=models.IntegerField(default=0, help_text='MRP must be smaller than or equal to Selling price.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.IntegerField(default=0, help_text='Selling Price must be greater than MRP.'),
        ),
    ]
