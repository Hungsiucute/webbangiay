# Generated by Django 5.1.2 on 2024-11-11 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_category_categori'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categori',
            new_name='Categorie',
        ),
    ]
