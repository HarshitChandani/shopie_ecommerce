# Generated by Django 4.0.2 on 2022-03-05 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0045_alter_productcategory_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='poster',
        ),
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(max_length=254, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='image',
            field=models.ImageField(max_length=254, upload_to=''),
        ),
    ]
