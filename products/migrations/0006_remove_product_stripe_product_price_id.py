# Generated by Django 4.2.1 on 2023-09-19 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_stripe_product_price_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stripe_product_price_id',
        ),
    ]
