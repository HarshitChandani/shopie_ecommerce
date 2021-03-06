# Generated by Django 4.0.2 on 2022-02-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sleeve_type',
            field=models.CharField(choices=[('full-sleeve', 'Full Sleeve'), ('half-sleeve', 'Half Sleeve'), ('3/4-sleeve', '3/4 Sleeve'), ('none', 'None')], max_length=100, verbose_name='Sleeve Length'),
        ),
    ]
