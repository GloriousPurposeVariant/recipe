# Generated by Django 3.2.9 on 2021-12-17 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='favourites',
            new_name='favorites',
        ),
    ]
