# Generated by Django 5.1.3 on 2024-11-26 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_is_sale_product_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
    ]
