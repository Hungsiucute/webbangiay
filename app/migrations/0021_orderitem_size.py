# Generated by Django 5.1.2 on 2024-12-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='S', max_length=2),
        ),
    ]
