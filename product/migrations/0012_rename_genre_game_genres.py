# Generated by Django 5.1.6 on 2025-02-11 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_review_site'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='genre',
            new_name='genres',
        ),
    ]
