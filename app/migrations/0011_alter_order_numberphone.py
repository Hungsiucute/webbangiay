# Generated by Django 5.1.2 on 2024-11-12 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_order_address_order_name_order_numberphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='numberphone',
            field=models.CharField(max_length=12, null=True),
        ),
    ]