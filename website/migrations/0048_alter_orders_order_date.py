# Generated by Django 4.0.2 on 2022-03-05 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0047_alter_brand_image_alter_occasion_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(null=True),
        ),
    ]
