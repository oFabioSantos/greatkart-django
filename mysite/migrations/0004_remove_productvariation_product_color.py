# Generated by Django 4.2.3 on 2023-10-13 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_productvariation_product_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariation',
            name='product_color',
        ),
    ]
