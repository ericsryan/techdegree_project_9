# Generated by Django 3.1.7 on 2021-04-05 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_menu_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='created_date',
            new_name='created_datetime',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='created_date',
            new_name='created_datetime',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='expiration_date',
            new_name='expiration_datetime',
        ),
    ]