# Generated by Django 5.1.2 on 2024-11-15 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_delete_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventory_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='purchased_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='remaining_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
